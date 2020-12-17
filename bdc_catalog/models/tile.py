#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
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

    grs = relationship('GridRefSys')

    __table_args__ = (
        Index(None, 'id'),
        Index(None, name),
        Index(None, grid_ref_sys_id),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
