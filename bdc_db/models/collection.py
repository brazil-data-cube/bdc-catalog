#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .base_sql import BaseModel


class Collection(BaseModel):
    __tablename__ = 'collections'

    id = Column(String(20), primary_key=True)
    temporal_composition_schema_id = Column(ForeignKey('temporal_composition_schemas.id'), nullable=True)
    raster_size_schema_id = Column(ForeignKey('raster_size_schemas.id'), nullable=True)
    composite_function_schema_id = Column(ForeignKey('composite_function_schemas.id'), nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), nullable=False)
    sensor = Column(String(40), nullable=True)
    geometry_processing = Column(String(16), nullable=True)
    radiometric_processing = Column(String(40), nullable=True)
    description = Column(String(250), nullable=False)
    oauth_scope = Column(String(250), nullable=True)
    is_cube = Column(Boolean, nullable=True, default=False)
    bands_quicklook = Column(String(250), nullable=True)
    license = Column(String(250), nullable=True)

    grs_schema = relationship('GrsSchema')
    composite_function_schemas = relationship('CompositeFunctionSchema')
    raster_size_schemas = relationship('RasterSizeSchema')
    temporal_composition_schema = relationship('TemporalCompositionSchema')
