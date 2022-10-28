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

"""Model for table ``bdc.applications``."""

from bdc_db.sqltypes import JSONB
from sqlalchemy import Column, Integer, String, UniqueConstraint

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel


class Processor(BaseModel):
    """Represent the STAC extension for Processing: Processor.

    See More in `Processing Extension Specification <https://github.com/stac-extensions/processing>`_.
    """

    __tablename__ = 'processors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    facility = Column(String(255), nullable=False)
    level = Column(String(32), nullable=False)
    version = Column(String(32), nullable=False)
    uri = Column(String(255))
    metadata_ = Column('metadata', JSONB('bdc-catalog/processor-metadata.json'),
                       comment='Follow the JSONSchema @jsonschemas/bdc-catalog/processor-metadata.json')

    __table_args__ = (
        UniqueConstraint(name, version),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
