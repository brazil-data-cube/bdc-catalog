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

"""Represent a basic example how to create a basic collection using class instance."""

from bdc_catalog import BDCCatalog
from bdc_catalog.models import Collection
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bdc'
BDCCatalog(app)

with app.app_context():
    collection = Collection()
    collection.name = 'S2_L1C'
    collection.version = '1'
    collection.title = 'Sentinel-2 - MSI - Level-1C'
    collection.properties = {
        "platform": "sentinel-2",
        "instruments": [
            "MSI"
        ]
    }
    collection.category = 'eo'
    collection.collection_type = 'collection'
    collection.keywords = ["eo", "sentinel", "msi"]
    collection.is_available = True
    collection.save()
