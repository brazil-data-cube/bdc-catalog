#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import (Column, Enum, ForeignKey, Index, Integer, Numeric,
                        String, Text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base_sql import BaseModel

name_data_type = 'data_type'
options_data_type = ('uint8', 'int8', 'uint16', 'int16', 'uint32', 'int32', 'float32', 'float64')
enum_data_type = Enum(*options_data_type, name=name_data_type)


class Band(BaseModel):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    common_name = Column(String(255), nullable=False)
    description = Column(Text)
    min = Column(Numeric)
    max = Column(Numeric)
    nodata = Column(Numeric)
    scale = Column(Numeric)
    resolution_x = Column(Numeric)
    resolution_y = Column(Numeric)
    center_wavelength = Column(Numeric)
    full_width_half_max = Column(Numeric)
    collection_id = Column(ForeignKey('collections.id', onupdate='CASCADE', ondelete='CASCADE'))
    resolution_unit_id = Column(ForeignKey('resolution_unit.id', onupdate='CASCADE', ondelete='CASCADE'))
    data_type = Column(enum_data_type)
    mime_type_id = Column(ForeignKey('mime_type.id', onupdate='CASCADE', ondelete='CASCADE'))
    _metadata = Column('metadata', JSONB, comment='Follow the JSONSchema @jsonschemas/band-metadata.json')

    collection = relationship('Collection')
    resolution_unit = relationship('ResolutionUnit')
    mime_type = relationship('MimeType')

    __table_args__ = (
        Index(None, collection_id),
        Index(None, name),
        Index(None, common_name),
        Index(None, mime_type_id),
    )
