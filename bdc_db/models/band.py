#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base_sql import BaseModel


class Band(BaseModel):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(20), unique=False, primary_key=True)
    collection_id = Column(ForeignKey('collections.id'), unique=False, primary_key=True)
    min = Column(Float)
    max = Column(Float)
    fill = Column(Integer)
    scale = Column(String(16))
    common_name = Column(String(16), nullable=False)
    data_type = Column(String(16))
    mime_type = Column(String(16))
    resolution_x = Column(Float(53), nullable=False)
    resolution_y = Column(Float(53), nullable=False)
    resolution_unit = Column(String(16), nullable=False)
    description = Column(String(64))

    collection = relationship('Collection')