#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
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

    Notes:
        This table is filled with trigger event on `Item`.
    """

    __tablename__ = 'timeline'

    collection_id = Column(ForeignKey(Collection.id, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    time_inst = Column(TIMESTAMP(timezone=True), nullable=False)

    collection = relationship('Collection')

    __table_args__ = (
        PrimaryKeyConstraint(collection_id, time_inst),
        # Index with collection_id & time instant reverse order (same as STAC)
        Index(None, collection_id, time_inst.desc()),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
