#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import Column, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from .base_sql import BaseModel


class MimeType(BaseModel):
    __tablename__ = 'mime_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)

    bands = relationship('Band')

    __table_args__ = (
        UniqueConstraint(name),
    )
