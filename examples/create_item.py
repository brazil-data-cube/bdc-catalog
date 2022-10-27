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

"""Represent a basic example how to create an Item instance.

Note:
    This file only describes way to register an Item.
    It requires that you have the scene used in your current directory.
"""

import shapely.geometry
from bdc_catalog import BDCCatalog
from bdc_catalog.models import Collection, Item
# We recommend to import bdc_catalog.utils.geom_to_wkb to transform shapely GEOM to WKB
from bdc_catalog.utils import geom_to_wkb
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bdc'
BDCCatalog(app)

with app.app_context():
    collection = Collection.get_by_id('S2_L1C-1')

    name = "S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627"
    geometry: shapely.geometry.Polygon = shapely.geometry.shape({
        "type": "Polygon",
        "coordinates": [[[-70.731002, -9.131078],
                         [-70.726482, -8.138363],
                         [-71.722423, -8.132908],
                         [-71.729545, -9.124947],
                         [-70.731002, -9.131078]]]
    })

    # Let's create a new Item definition
    item = Item(collection_id=collection.id, name=name)
    item.cloud_cover = 0
    item.start_date = item.end_date = "2021-05-27T15:07:21"
    item.footprint = geom_to_wkb(geometry, srid=4326)
    item.bbox = geom_to_wkb(geometry.envelope, srid=4326)
    item.is_available = True
    for band in ['B02.tif', 'B03.tif', 'B04.tif', 'thumbnail.png']:
        item.add_asset(name=band.split('.')[0],  # Use only name as asset key
                       file=f"S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627/{band}",
                       role=["data"],
                       href=f"/s2-l1c/19/L/BL/2021/S2A_MSIL1C_20210527T150721_1/{band}")
    item.save()
