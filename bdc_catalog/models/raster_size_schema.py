#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import Column, Float, String

from .base_sql import BaseModel


class RasterSizeSchema(BaseModel):
    __tablename__ = 'raster_size_schemas'

    id = Column(String(60), primary_key=True)
    raster_size_x = Column(Float(53), nullable=False)
    raster_size_y = Column(Float(53), nullable=False)
    raster_size_t = Column(Float(53))
    chunk_size_x = Column(Float(53), nullable=False)
    chunk_size_y = Column(Float(53), nullable=False)
    chunk_size_t = Column(Float(53))