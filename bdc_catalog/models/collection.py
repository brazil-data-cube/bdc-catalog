#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for the main table of image collections and data cubes."""

from typing import List, Optional, Union

from geoalchemy2 import Geometry
from bdc_db.sqltypes import JSONB
from lccs_db.models import LucClassificationSystem
from sqlalchemy import (ARRAY, TIMESTAMP, Boolean, Column, Enum, ForeignKey, Index,
                        Integer, PrimaryKeyConstraint, String,
                        Text, UniqueConstraint)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel, db
from .provider import Provider

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
    is_public = Column(Boolean(), nullable=False, default=True)
    is_available = Column(Boolean(), nullable=False, default=False)
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
        Index(None, is_public),
        Index(None, is_available),
        Index(None, start_date, end_date),
        dict(schema=BDC_CATALOG_SCHEMA),
    )

    @property
    def providers(self):
        """The list of providers relationship of Collection."""
        return CollectionsProviders.get_providers(self.id)

    @classmethod
    def get_by_id(cls, collection_id: Union[str, int]) -> 'Collection':
        """Retrieve a collection using the identifier or Collection Versioning."""
        where = []
        if isinstance(collection_id, str):
            name, version = collection_id.rsplit('-', 1)
            where.extend((Collection.name == name, Collection.version == version))
        else:
            where.append(Collection.id == collection_id)

        return cls.query().filter(*where).first_or_404(f'Collection {collection_id} not found')

    @hybrid_property
    def identifier(self):
        """Retrieve the Collection Identifier which refers to Name-Version."""
        return f'{self.name}-{self.version}'

    @identifier.expression
    def identifier(self):
        """Identifier for Name-Version used in SQLAlchemy queries."""
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