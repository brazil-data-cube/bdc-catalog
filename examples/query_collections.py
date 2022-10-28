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

"""Represent a basic example how to iterate over Collections in database.

The example includes all the way to retrieve collection using Identifier, availability and spatial temporal area.
"""

from bdc_catalog import BDCCatalog
from bdc_catalog.models import Collection
from flask import Flask
from shapely.geometry import box
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bdc'
BDCCatalog(app)

with app.app_context():
    # List all collections
    collections = (
        Collection.query()
        .all()
    )
    print(f"Collections: {','.join([c.identifier for c in collections])}")

    # List only available collections
    collections = (
        Collection.query()
        .filter(Collection.is_available.is_(True))
        .all()
    )
    print(f"Available Collections: {','.join([c.identifier for c in collections])}")

    # Retrieve a collection by identifier
    collection = Collection.get_by_id("S2_L1C-1")  # or Collection.get_by_id(Id)
    print(f"Collection: {collection.identifier}")

    # Or verbose way
    collection = (
        Collection.query()
        .filter(Collection.identifier == "S2_L1C-1")  # or Collection.id == Id
        .first()
    )

    # Filter by area and temporal axis
    roi = box(-54, -12, -53, -11)
    collections = (
        Collection.query()
        .filter(func.ST_Intersects(Collection.spatial_extent, roi),
                Collection.start_date >= '2022-01-01')
        .all()
    )
    print(f"Collections Filter ({roi.wkt}): {','.join([c.identifier for c in collections])}")
