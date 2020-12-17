#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for table ``bdc.providers``."""

from sqlalchemy import Column, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel


class Provider(BaseModel):
    """Model for table ``bdc.providers``.

    A provider consists in a maintainer, organization that offer the data to be downloaded.
    In the Brazil Data Cube context, they may be: ``USGS``, ``Copernicus``, ``Google Public Datasets``, etc.
    Each provider should have their own credentials associated to be automatically configurable
    by BDC tools."""

    __tablename__ = 'providers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    description = Column(Text)
    uri = Column(String(255))
    credentials = Column(JSONB, comment='Follow the JSONSchema @jsonschemas/provider-credentials.json')

    __table_args__ = (
        Index(None, name),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
