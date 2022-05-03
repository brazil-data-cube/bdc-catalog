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

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel


class Processor(BaseModel):
    """Represent the STAC extension for Processing: Processor.

    See More in `Processing Extension Specification <https://github.com/stac-extensions/processing>`_.
    """

    __tablename__ = 'processors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    facility = Column(String(255), nullable=False)
    level = Column(String(32), nullable=False)
    version = Column(String(32), nullable=False)
    uri = Column(String(255))
    metadata_ = Column('metadata', JSONB('bdc-catalog/processor.json'),
                       comment='Follow the JSONSchema @jsonschemas/application-metadata.json')

    __table_args__ = (
        UniqueConstraint(name, version),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
