#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from geoalchemy2 import Geometry
from sqlalchemy import (Column, Index, Integer, ForeignKey,
                        Numeric, String, TIMESTAMP)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from .base_sql import BaseModel


class Item(BaseModel):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    collection_id = Column(ForeignKey('collections.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    tile_id = Column(ForeignKey('tiles.id', onupdate='CASCADE', ondelete='CASCADE'))
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    cloud_cover = Column(Numeric)
    assets = Column(JSONB, comment='Follow the JSONSchema @jsonschemas/item-assets.json')
    _metadata = Column('metadata', JSONB, comment='Follow the JSONSchema @jsonschemas/item-metadata.json')
    provider_id = Column(ForeignKey('providers.id', onupdate='CASCADE', ondelete='CASCADE'))
    application_id = Column(ForeignKey('applications.id', onupdate='CASCADE', ondelete='CASCADE'))
    geom = Column(Geometry(geometry_type='Polygon', srid=4326, spatial_index=False))
    min_convex_hull = Column(Geometry(geometry_type='Polygon', srid=4326, spatial_index=False))

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
    )