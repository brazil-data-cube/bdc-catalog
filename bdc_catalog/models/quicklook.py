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

from .base_sql import BaseModel


class Quicklook(BaseModel):
    """Model for collection QuickLook info."""

    __tablename__ = 'quicklook'

    collection_id = Column(ForeignKey('collections.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    red = Column(ForeignKey('bands.id', onupdate='CASCADE', ondelete='CASCADE'))
    green = Column(ForeignKey('bands.id', onupdate='CASCADE', ondelete='CASCADE'))
    blue = Column(ForeignKey('bands.id', onupdate='CASCADE', ondelete='CASCADE'))

    collection = relationship('Collection')
