#
# This file is part of BDC-Catalog.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Model for the main table of image collections and data cubes."""

from typing import List, Union

from bdc_db.sqltypes import JSONB
from geoalchemy2 import Geometry
from lccs_db.models import LucClassificationSystem
from sqlalchemy import (ARRAY, TIMESTAMP, Boolean, Column, Enum, ForeignKey,
                        Index, Integer, PrimaryKeyConstraint, String, Text,
                        UniqueConstraint)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel, db
from .provider import Provider
from .role import Role

name_collection_type = 'collection_type'
options_collection_type = ('cube', 'collection', 'classification', 'mosaic')
enum_collection_type = Enum(*options_collection_type, name=name_collection_type)
enum_provider_role_type = Enum('licensor', 'producer', 'processor', 'host', name='provider_role_type')
enum_collection_category = Enum('eo', 'sar', 'lidar', 'unknown', name='collection_category_type')


class Collection(BaseModel):
    """Model for the main table of image collections and data cubes."""

    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment='Collection name internally.')
    title = Column(String(255), nullable=False, comment='A human-readable string naming for collection.')
    description = Column(Text)
    temporal_composition_schema = Column(JSONB('bdc-catalog/collection-temporal-composition-schema.json'),
                                         comment='Follow the JSONSchema @jsonschemas/collection-temporal-composition-schema.json')
    composite_function_id = Column(
        ForeignKey(f'{BDC_CATALOG_SCHEMA}.composite_functions.id', onupdate='CASCADE', ondelete='CASCADE'),
        comment='Function schema identifier. Used for data cubes.')
    grid_ref_sys_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.grid_ref_sys.id', onupdate='CASCADE', ondelete='CASCADE'))
    classification_system_id = Column(ForeignKey(LucClassificationSystem.id, onupdate='CASCADE', ondelete='CASCADE'))
    collection_type = Column(enum_collection_type, nullable=False)
    metadata_ = Column('metadata', JSONB('bdc-catalog/collection-metadata.json'),
                       comment='Follow the JSONSchema @jsonschemas/collection-metadata.json')
    keywords = Column('keywords', ARRAY(String))
    properties = Column('properties', JSONB('bdc-catalog/collection-properties.json'),
                        comment='Contains the properties offered by STAC collections')
    summaries = Column('summaries', JSONB('bdc-catalog/collection-summaries.json'),
                       comment='Contains the STAC Collection summaries.')
    item_assets = Column('item_assets', JSONB('bdc-catalog/collection-item-assets.json'),
                         comment='Contains the STAC Extension Item Assets.')
    is_available = Column(Boolean(), nullable=False, default=False, server_default='False')
    category = Column(enum_collection_category, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    spatial_extent = Column(Geometry(geometry_type='Polygon', srid=4326, spatial_index=False))
    version = Column(String, nullable=False)
    version_predecessor = Column(ForeignKey(id, onupdate='CASCADE', ondelete='CASCADE'))
    version_successor = Column(ForeignKey(id, onupdate='CASCADE', ondelete='CASCADE'))

    grs = relationship('GridRefSys')
    composite_function = relationship('CompositeFunction')
    bands = relationship('Band', back_populates='collection')
    quicklook = relationship('Quicklook')
    timeline = relationship('Timeline')
    # Joined Eager Loading. Default is Left Outer Join to lead object that does not refer to a related row.
    classification_system = relationship('LucClassificationSystem', lazy='joined')

    __table_args__ = (
        UniqueConstraint('name', 'version'),
        Index(None, grid_ref_sys_id),
        Index(None, name),
        Index(None, spatial_extent, postgresql_using='gist'),
        Index(None, classification_system_id),
        Index(None, category),
        Index(None, is_available),
        Index(None, start_date, end_date),
        dict(schema=BDC_CATALOG_SCHEMA),
    )

    @property
    def providers(self) -> List['CollectionsProviders']:
        """The list of providers relationship of Collection.

        .. versionadded:: 1.0.0
        """
        return CollectionsProviders.get_providers(self.id)

    @classmethod
    def get_by_id(cls, collection_id: Union[str, int]) -> 'Collection':
        """Retrieve a collection using the identifier or Collection Versioning.

        .. versionadded:: 1.0.0

        Args:
            collection_id: The collection id (int) or the identifier (composed by Name-Version).

        Raises:
            werkzeug.exceptions.NotFound: When collection not found.
        """
        where = []
        if isinstance(collection_id, str):
            where.append(Collection.identifier == collection_id)
        else:
            where.append(Collection.id == collection_id)

        return cls.query().filter(*where).first_or_404(f'Collection {collection_id} not found')

    @hybrid_property
    def identifier(self):
        """Retrieve the Collection Identifier which refers to Name-Version."""
        return f'{self.name}-{self.version}'

    @identifier.expression
    def identifier(self):
        """Identifier for Name-Version used in SQLAlchemy queries.

        .. versionadded:: 1.0.0

        Example:
            >>> collection = Collection.query().filter(Collection.identifier == 'S2_L2A-1').first() # doctest: +SKIP
            >>> collection.identifier  # doctest: +SKIP
            S2_L2A-1
        """
        return func.concat(self.name, '-', self.version)


class CollectionSRC(BaseModel):
    """Model for collection provenance/lineage."""

    __tablename__ = 'collection_src'

    collection_id = db.Column('collection_id', db.Integer(),
              db.ForeignKey(Collection.id, onupdate='CASCADE', ondelete='CASCADE'),
              nullable=False)

    collection_src_id = db.Column('collection_src_id', db.Integer(),
              db.ForeignKey(Collection.id, onupdate='CASCADE', ondelete='CASCADE'),
              nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(collection_id, collection_src_id),
        dict(schema=BDC_CATALOG_SCHEMA),
    )


class CollectionsProviders(BaseModel):
    """Track the available data providers for an image collection.

    This model integrates with STAC Providers spec."""

    __tablename__ = 'collections_providers'

    provider_id = Column('provider_id', db.Integer(),
                         ForeignKey(Provider.id, onupdate='CASCADE', ondelete='CASCADE'),
                         nullable=False, primary_key=True)

    collection_id = Column('collection_id',
                           db.Integer(),
                           ForeignKey(Collection.id, onupdate='CASCADE', ondelete='CASCADE'),
                           nullable=False, primary_key=True)

    roles = Column(ARRAY(enum_provider_role_type), nullable=False)

    __table_args__ = (
        Index(None, roles),
        dict(schema=BDC_CATALOG_SCHEMA),
    )

    provider = relationship(Provider)
    collection = relationship(Collection)

    @classmethod
    def get_providers(cls, collection_id: Union[int, str]) -> List['CollectionsProviders']:
        """Retrieve the Providers related to the given collection.

        .. versionadded:: 1.0.0

        Note:
            You may use both Collection.id or `CollectionName-Version` as identifier.
        """
        join = []
        if isinstance(collection_id, str):
            where = [func.concat(Collection.name, '-', Collection.version) == collection_id]
            join.append((Collection, CollectionsProviders.collection_id == Collection.id))
        else:
            where = [CollectionsProviders.collection_id == collection_id]

        query = (
            db.session.query(CollectionsProviders)
        )
        for model, condition in join:
            query = query.join(model, condition)

        entries = query.filter(*where).all()

        return entries

    def to_dict(self) -> dict:
        """Retrieve the relationship as Python Dictionary.

        Note:
            The properties follows the STAC specification in `Provider Object <https://github.com/radiantearth/stac-spec/blob/v1.0.0/collection-spec/collection-spec.md#provider-object>`_.
        """
        return dict(name=self.provider.name, description=self.provider.description,
                    url=self.provider.url, roles=self.roles)


class CollectionRole(BaseModel):
    """Model to represent the link between Collection and Role."""

    __tablename__ = 'collections_roles'

    collection_id = db.Column('collection_id', db.Integer(),
                              db.ForeignKey(Collection.id, onupdate='CASCADE', ondelete='CASCADE'),
                              nullable=False)

    role_id = db.Column('role_id', db.Integer(),
                        db.ForeignKey(Role.id, onupdate='CASCADE', ondelete='CASCADE'),
                        nullable=False)

    collection = relationship('Collection', lazy='joined', foreign_keys=[collection_id])
    role = relationship('Role', lazy='joined')

    __table_args__ = (
        PrimaryKeyConstraint(collection_id, role_id),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
