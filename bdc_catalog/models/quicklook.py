#
# This file is part of BDC-Catalog.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
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
