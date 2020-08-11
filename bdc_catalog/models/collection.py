#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from geoalchemy2 import Geometry
from sqlalchemy import (Column, ForeignKey, String, Enum, Text, Integer,
                        UniqueConstraint, Index, TIMESTAMP, Boolean, SmallInteger, PrimaryKeyConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from .base_sql import BaseModel, db

name_collection_type = 'collection_type'
options_collection_type = ('cube', 'collection')
enum_collection_type = Enum(*options_collection_type, name=name_collection_type)


class Collection(BaseModel):
    """Define the collection structure for Brazil Data Cube."""

    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment='Collection name internally.')
    title = Column(String(255), nullable=False, comment='A human-readable string naming for collection.')
    description = Column(Text)
    temporal_composition_schema = Column(JSONB, comment='Follow the JSONSchema @jsonschemas/collection-temporal-composition-schema.json')
    composite_function_id = Column(
        ForeignKey('composite_functions.id', onupdate='CASCADE', ondelete='CASCADE'),
        comment='Function schema identifier. Used for data cubes.')
    grid_ref_sys_id = Column(ForeignKey('grid_ref_sys.id', onupdate='CASCADE', ondelete='CASCADE'))
    instrument = Column(JSONB, comment='Follow the JSONSchema @jsonschemas/collection-instrument.json')
    collection_type = Column(enum_collection_type, nullable=False)
    datacite = Column(JSONB, comment='Follow the JSONSchema @jsonschemas/collection-datacite.json')
    _metadata = Column('metadata', JSONB, comment='Follow the JSONSchema @jsonschemas/collection-metadata.json')
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    extent = Column(Geometry(geometry_type='Polygon', srid=4326, spatial_index=False))
    version = Column(Integer, nullable=False)
    version_predecessor = Column(ForeignKey('collections.id', onupdate='CASCADE', ondelete='CASCADE'))
    version_successor = Column(ForeignKey('collections.id', onupdate='CASCADE', ondelete='CASCADE'))

    grs = relationship('GridRefSys')
    composite_function = relationship('CompositeFunction')

    __table_args__ = (
        UniqueConstraint('name', 'version'),
        Index(None, grid_ref_sys_id),
        Index(None, name),
        Index(None, extent, postgresql_using='gist'),
    )


class CollectionSRC(BaseModel):
    __tablename__ = 'collection_src'

    collection_id = db.Column('collection_id', db.Integer(),
              db.ForeignKey(Collection.id, onupdate='CASCADE', ondelete='CASCADE'),
              nullable=False)

    collection_src_id = db.Column('collection_src_id', db.Integer(),
              db.ForeignKey(Collection.id, onupdate='CASCADE', ondelete='CASCADE'),
              nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(collection_id, collection_src_id),
    )


class CollectionsProviders(BaseModel):
    __tablename__ = 'collections_providers'

    provider_id = Column('provider_id', db.Integer(),
                         ForeignKey('providers.id', onupdate='CASCADE', ondelete='CASCADE'),
                         nullable=False, primary_key=True)

    collection_id = Column('collection_id',
                           db.Integer(),
                           ForeignKey(Collection.id, onupdate='CASCADE', ondelete='CASCADE'),
                           nullable=False, primary_key=True)

    active = Column(Boolean(), nullable=False, default=True)
    priority = Column(SmallInteger(), nullable=False)
