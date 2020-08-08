#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import Column, String

from .base_sql import BaseModel


class TemporalCompositionSchema(BaseModel):
    __tablename__ = 'temporal_composition_schemas'

    id = Column(String(20), primary_key=True)
    temporal_composite_unit = Column(String(16), nullable=False)
    temporal_schema = Column(String(16), nullable=False)
    temporal_composite_t = Column(String(16), nullable=False)