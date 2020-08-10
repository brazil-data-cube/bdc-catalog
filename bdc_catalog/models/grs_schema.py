#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import relationship

from .base_sql import BaseModel


class GrsSchema(BaseModel):
    __tablename__ = 'grs_schemas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    table_id = Column(OID, nullable=False)

    __table_args__ = (
        UniqueConstraint(name),
    )

    tiles = relationship('Tile')
