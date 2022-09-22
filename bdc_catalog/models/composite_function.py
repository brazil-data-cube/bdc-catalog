#
# This file is part of BDC-Catalog.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
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
