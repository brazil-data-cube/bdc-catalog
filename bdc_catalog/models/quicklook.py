#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for collection QuickLook info."""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel


class Quicklook(BaseModel):
    """Model for collection QuickLook info."""

    __tablename__ = 'quicklook'
    __table_args__ = dict(
        schema=BDC_CATALOG_SCHEMA
    )

    collection_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.collections.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    red = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.bands.id', onupdate='CASCADE', ondelete='CASCADE'))
    green = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.bands.id', onupdate='CASCADE', ondelete='CASCADE'))
    blue = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.bands.id', onupdate='CASCADE', ondelete='CASCADE'))

    collection = relationship('Collection', back_populates='quicklook')
