#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for the image item of a collection."""

from geoalchemy2 import Geometry
from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Index, Integer, Numeric,
                        String)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from ..config import BDC_CATALOG_SCHEMA
from .application import Application
from .base_sql import BaseModel, db
from .collection import Collection
from .provider import Provider
from .tile import Tile


class SpatialRefSys(db.Model):
    """Auxiliary model for the PostGIS spatial_ref_sys table."""

    __tablename__ = 'spatial_ref_sys'
    __table_args__ = ({"schema": "public"})

    srid = Column(Integer, primary_key=True)
    auth_name = Column(String)
    auth_srid = Column(Integer)
    srtext = Column(String)
    proj4text = Column(String)


class Item(BaseModel):
    """Model for the image item of a collection."""

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    collection_id = Column(ForeignKey(Collection.id, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    tile_id = Column(ForeignKey(Tile.id, onupdate='CASCADE', ondelete='CASCADE'))
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    cloud_cover = Column(Numeric)
    assets = Column(JSONB, comment='Follow the JSONSchema @jsonschemas/item-assets.json')
    _metadata = Column('metadata', JSONB, comment='Follow the JSONSchema @jsonschemas/item-metadata.json')
    provider_id = Column(ForeignKey(Provider.id, onupdate='CASCADE', ondelete='CASCADE'))
    application_id = Column(ForeignKey(Application.id, onupdate='CASCADE', ondelete='CASCADE'))
    geom = Column(Geometry(geometry_type='Polygon', srid=4326, spatial_index=False))
    min_convex_hull = Column(Geometry(geometry_type='Polygon', srid=4326, spatial_index=False))
    srid = Column(Integer, ForeignKey('public.spatial_ref_sys.srid', onupdate='CASCADE', ondelete='CASCADE'))

    collection = relationship('Collection')
    tile = relationship('Tile')
    provider = relationship('Provider')
    application = relationship('Application')

    __table_args__ = (
        Index(None, cloud_cover),
        Index(None, collection_id),
        Index(None, 'geom', postgresql_using='gist'),
        Index(None, min_convex_hull, postgresql_using='gist'),
        Index(None, name),
        Index(None, provider_id),
        Index('idx_items_start_date_end_date', start_date, end_date),
        Index(None, tile_id),
        Index(None, start_date.desc()),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
