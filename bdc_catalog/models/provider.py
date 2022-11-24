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

"""Model for table ``bdc.providers``."""

from sqlalchemy import Column, Index, Integer, String, Text
from sqlalchemy.orm import relationship

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
