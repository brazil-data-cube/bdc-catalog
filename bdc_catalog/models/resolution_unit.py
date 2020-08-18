#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for table ``bdc.resolution_unit``."""

from sqlalchemy import Column, Integer, String, Text, UniqueConstraint

from .base_sql import BaseModel


class ResolutionUnit(BaseModel):
    """Model for table ``bdc.resolution_unit``."""

    __tablename__ = 'resolution_unit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    symbol = Column(String(3))
    description = Column(Text)