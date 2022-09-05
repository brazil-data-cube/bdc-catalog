#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for collection QuickLook info."""

from typing import Tuple

from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.orm import relationship

from ..config import BDC_CATALOG_SCHEMA
from .band import Band
from .base_sql import BaseModel


class Quicklook(BaseModel):
    """Model for collection QuickLook info."""

    __tablename__ = 'quicklook'

    collection_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.collections.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    red = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.bands.id', onupdate='CASCADE', ondelete='CASCADE'))
    green = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.bands.id', onupdate='CASCADE', ondelete='CASCADE'))
    blue = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.bands.id', onupdate='CASCADE', ondelete='CASCADE'))

    collection = relationship('Collection', back_populates='quicklook')

    __table_args__ = (
        Index(None, collection_id),
        dict(schema=BDC_CATALOG_SCHEMA),
    )

    def get_bands(self) -> Tuple[Band, Band, Band]:
        """Retrieve the Band object reference for each RGB channel."""
        red = Band.query().filter(Band.id == self.red).first()
        green = Band.query().filter(Band.id == self.green).first()
        blue = Band.query().filter(Band.id == self.blue).first()

        return red, green, blue
