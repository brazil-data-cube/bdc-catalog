#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for table ``bdc.providers``."""

from sqlalchemy import Column, Index, Integer, String, Text

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel


class Provider(BaseModel):
    """Model for table ``bdc.providers``.

    This model provides information about the provider. A provider is any of the organizations that captures, procecesses
    or host the content of the collection.

    See more in `STAC Provider Object <https://github.com/radiantearth/stac-spec/blob/v1.0.0/collection-spec/collection-spec.md#provider-object>`_
    """

    __tablename__ = 'providers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    description = Column(Text)
    url = Column(String(255))

    __table_args__ = (
        Index(None, name),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
