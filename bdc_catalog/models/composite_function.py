#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for table ``bdc.composite_functions``."""

from sqlalchemy import Column, Integer, String, Text

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel


class CompositeFunction(BaseModel):
    """Model for table ``bdc.composite_functions``.

    A composition function consists in a function that chooses a pixel value,
    according to a heuristic, from a set of pixels contained within a time interval.

    The functions `Stack`, `Median` and `Identity` are offered by default in Brazil Data Cube.
    """

    __tablename__ = 'composite_functions'
    __table_args__ = dict(
        schema=BDC_CATALOG_SCHEMA
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    alias = Column(String(6), nullable=False, unique=True)
