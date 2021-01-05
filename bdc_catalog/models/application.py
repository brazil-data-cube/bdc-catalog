#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for table ``bdc.applications``."""

from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel
from .item import Item


class Application(BaseModel):
    """Define an application to catalog items on Brazil Data Cube model."""

    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    version = Column(String(32), nullable=False)
    uri = Column(String(255))
    _metadata = Column('metadata', JSONB, comment='Follow the JSONSchema @jsonschemas/application-metadata.json')

    items = relationship(Item)

    __table_args__ = (
        UniqueConstraint(name, version),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
