#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from geoalchemy2 import Geometry
from sqlalchemy import Column, Float, ForeignKey, Index, String
from sqlalchemy.orm import relationship

from .base_sql import BaseModel


class Tile(BaseModel):
    __tablename__ = 'tiles'
    __table_args__ = (
        Index('idx_tiles_geom_wgs84', 'geom_wgs84', postgres_using='gist'),
        Index('idx_tiles_geom', 'geom', postgres_using='gist'),
    )

    id = Column(String(20), primary_key=True, nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), primary_key=True, nullable=False)
    geom_wgs84 = Column(Geometry(spatial_index=False))
    geom = Column(Geometry(spatial_index=False))
    min_x = Column(Float)
    max_x = Column(Float)
    min_y = Column(Float)
    max_x = Column(Float)

    grs_schema = relationship('GrsSchema')