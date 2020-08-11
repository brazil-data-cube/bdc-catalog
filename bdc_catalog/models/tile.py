#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import Column, ForeignKey, Index, String, Integer
from sqlalchemy.orm import relationship

from .base_sql import BaseModel


class Tile(BaseModel):
    __tablename__ = 'tiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    grid_ref_sys_id = Column(ForeignKey('grid_ref_sys.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    name = Column(String(20), nullable=False)

    grs = relationship('GridRefSys')

    __table_args__ = (
        Index(None, 'id'),
        Index(None, name),
        Index(None, grid_ref_sys_id)
    )
