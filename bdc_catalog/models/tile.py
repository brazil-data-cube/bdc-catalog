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

"""Model for table ``bdc.tile``."""

from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel


class Tile(BaseModel):
    """Model for table ``bdc.tile``.

    A tile is an element of a GRS, associated with a unique code, that represents a geographic region.
    """

    __tablename__ = 'tiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    grid_ref_sys_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.grid_ref_sys.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    name = Column(String(20), nullable=False)
    """The tile name (path row) identifier."""

    grs = relationship('GridRefSys', back_populates='tiles')

    __table_args__ = (
        Index(None, 'id'),
        Index(None, name),
        Index(None, grid_ref_sys_id),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
