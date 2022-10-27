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

"""Represent a basic example how to iterate over items in database.

The example includes all the way to retrieve items using availability, cloud cover factor
and spatial temporal area.
"""

from bdc_catalog import BDCCatalog
from bdc_catalog.models import Collection, Item, Tile, db
from flask import Flask
from shapely.geometry import box
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bdc'
BDCCatalog(app)

with app.app_context():
    # Use collection as reference
    collection = Collection.get_by_id('S2_L1C-1')

    items = (
        Item.query()
        .filter(Item.collection_id == collection.id)
        .all()
    )
    print(f'Items: {[i.name for i in items[:10]]}')

    items = (
        Item.query()
        .filter(Item.collection_id == collection.id,
                Item.cloud_cover <= 50,
                Item.is_available.is_(True))
        .order_by(Item.start_date.desc())
        .all()
    )
    print(f'Items (cloud <= 50%): {[i.name for i in items[:10]]}')

    items = (
        db.session.query(Item)
        .join(Tile, Tile.id == Item.tile_id)
        .filter(Item.collection_id == collection.id,
                Tile.name == '23LLG')
        .order_by(Item.start_date.desc())
        .all()
    )
    print(f'Items (from tile): {[i.name for i in items[:10]]}')

    roi = box(-54, -12, -53, -11)
    items = (
        db.session.query(Item)
        .join(Tile, Tile.id == Item.tile_id)
        .filter(func.ST_Intersects(Item.bbox, roi),  # Intersect by ROI
                Item.start_date >= '2022-01-01')
        .order_by(Item.start_date.desc())
        .all()
    )
    print(f'Items (from tile): {[i.name for i in items[:10]]}')