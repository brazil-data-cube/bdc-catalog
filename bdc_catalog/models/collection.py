#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for the main table of image collections and data cubes."""

from geoalchemy2 import Geometry
from lccs_db.models import LucClassificationSystem
from sqlalchemy import (TIMESTAMP, Boolean, Column, Enum, ForeignKey, Index,
                        Integer, PrimaryKeyConstraint, SmallInteger, String,
                        Text, UniqueConstraint)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel, db
from .provider import Provider

name_collection_type = 'collection_type'
options_collection_type = ('cube', 'collection', 'classification', 'mosaic')
enum_collection_type = Enum(*options_collection_type, name=name_collection_type)


class Collection(BaseModel):
    """Model for the main table of image collections and data cubes."""

    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment='Collection name internally.')
    title = Column(String(255), nullable=False, comment='A human-readable string naming for collection.')
    description = Column(Text)
    temporal_composition_schema = Column(JSONB, comment='Follow the JSONSchema @jsonschemas/collection-temporal-composition-schema.json')
    composite_function_id = Column(
        ForeignKey(f'{BDC_CATALOG_SCHEMA}.composite_functions.id', onupdate='CASCADE', ondelete='CASCADE'),
        comment='Function schema identifier. Used for data cubes.')
    grid_ref_sys_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.grid_ref_sys.id', onupdate='CASCADE', ondelete='CASCADE'))
    classification_system_id = Column(ForeignKey(LucClassificationSystem.id, onupdate='CASCADE', ondelete='CASCADE'))
    collection_type = Column(enum_collection_type, nullable=False)
    _metadata = Column('metadata', JSONB, comment='Follow the JSONSchema @jsonschemas/collection-metadata.json')
    is_public = Column(Boolean(), nullable=False, default=True)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    extent = Column(Geometry(geometry_type='Polygon', srid=4326, spatial_index=False))
    version = Column(Integer, nullable=False)
    version_predecessor = Column(ForeignKey(id, onupdate='CASCADE', ondelete='CASCADE'))
    version_successor = Column(ForeignKey(id, onupdate='CASCADE', ondelete='CASCADE'))
    srid = Column(Integer, ForeignKey('public.spatial_ref_sys.srid', onupdate='CASCADE', ondelete='CASCADE'))

    grs = relationship('GridRefSys')
    composite_function = relationship('CompositeFunction')
    bands = relationship('Band')
    quicklook = relationship('Quicklook')
    timeline = relationship('Timeline')
    # Joined Eager Loading. Default is Left Outer Join to lead object that does not refer to a related row.
    classification_system = relationship('LucClassificationSystem', lazy='joined')

    __table_args__ = (
        UniqueConstraint('name', 'version'),
        Index(None, grid_ref_sys_id),
        Index(None, name),
        Index(None, extent, postgresql_using='gist'),
        Index(None, classification_system_id),
        Index(None, srid),
        dict(schema=BDC_CATALOG_SCHEMA),
    )


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
    """Track the available data providers for an image collection."""

    __tablename__ = 'collections_providers'
    __table_args__ = dict(
        schema=BDC_CATALOG_SCHEMA
    )

    provider_id = Column('provider_id', db.Integer(),
                         ForeignKey(Provider.id, onupdate='CASCADE', ondelete='CASCADE'),
                         nullable=False, primary_key=True)

    collection_id = Column('collection_id',
                           db.Integer(),
                           ForeignKey(Collection.id, onupdate='CASCADE', ondelete='CASCADE'),
                           nullable=False, primary_key=True)

    active = Column(Boolean(), nullable=False, default=True)
    priority = Column(SmallInteger(), nullable=False)
