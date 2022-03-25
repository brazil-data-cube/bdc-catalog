#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for table ``bdc.composite_functions``."""

from sqlalchemy import Column, Index, Integer, String

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel


class Location(BaseModel):
    """Model for table ``bdc.locations``.

    This abstraction represents the both Internal and Public URL of physical data located.
    """

    __tablename__ = 'collection_locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_uri = Column(String(255), nullable=False)
    private_uri = Column(String(255), nullable=False)

    __table_args__ = (
        Index(None, public_uri,),
        Index(None, private_uri,),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
