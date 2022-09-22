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

"""Represent a basic example how to initialize BDC-Catalog module inside a flask application.

In order to list a collection, make sure you have load minimal collections inside ``fixtures``folder
with command line from :py:meth:`bdc_catalog.cli.load_data`::

    bdc-catalog load-data --ifile examples/fixtures/sentinel-2.json
"""

from flask import Flask

from bdc_catalog import BDCCatalog
from bdc_catalog.models import Collection

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bdcdb'

BDCCatalog(app)

with app.app_context():
    # Retrieve all collections (Available Only)
    collections = Collection.query().filter(Collection.is_available.is_(True)).all()

    print('Collections available:', ", ".join(c.identifier for c in collections))
