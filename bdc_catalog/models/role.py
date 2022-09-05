#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for table ``bdc.role``."""

from sqlalchemy import Column, Index, Integer, String, Text
from sqlalchemy.orm import relationship

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel


class Role(BaseModel):
    """Model for table ``bdc.role``.

    The role model consists in a basic way to specify a required roles to access collections/items.
    These values are used by BDC-Catalog NGINX plugin in order to validate user access.
    """

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)
    description = Column(Text)

    __table_args__ = (
        Index(None, name),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
