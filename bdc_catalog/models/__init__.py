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

"""SQLAlchemy model classes for BDC-Catalog."""

from .band import Band, BandSRC
from .base_sql import db
from .collection import (Collection, CollectionRole, CollectionsProviders,
                         CollectionSRC)
from .composite_function import CompositeFunction
from .grid_ref_sys import GridRefSys
from .item import Item, ItemsProcessors, SpatialRefSys
from .mime_type import MimeType
from .processor import Processor
from .provider import Provider
from .quicklook import Quicklook
from .resolution_unit import ResolutionUnit
from .role import Role
from .tile import Tile
from .timeline import Timeline

__all__ = (
    'db',
    'Band',
    'BandSRC',
    'Collection',
    'CollectionRole',
    'CollectionSRC',
    'CollectionsProviders',
    'CompositeFunction',
    'GridRefSys',
    'Item',
    'ItemsProcessors',
    'MimeType',
    'Processor',
    'Provider',
    'Quicklook',
    'ResolutionUnit',
    'Role',
    'SpatialRefSys',
    'Tile',
    'Timeline',
)
