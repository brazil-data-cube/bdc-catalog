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

"""Model for table ``bdc.timeline``."""

from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Index,
                        PrimaryKeyConstraint)
from sqlalchemy.orm import relationship

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel
from .collection import Collection


class Timeline(BaseModel):
    """Model for timeline.

    Track the entire time line for a collection.

    Notes:
        This table is filled with trigger event on `Item`.
    """

    __tablename__ = 'timeline'

    collection_id = Column(ForeignKey(Collection.id, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    time_inst = Column(TIMESTAMP(timezone=True), nullable=False)

    collection = relationship('Collection', back_populates='timeline')

    __table_args__ = (
        PrimaryKeyConstraint(collection_id, time_inst),
        # Index with collection_id & time instant reverse order (same as STAC)
        Index(None, collection_id, time_inst.desc()),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
