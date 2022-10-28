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

"""Represent a basic example how to create a mime type objects that will be used by collection bands.

The example includes all the common types used along Brazil Data Cube applications.
"""

from bdc_catalog import BDCCatalog
from bdc_catalog.models import MimeType
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bdc'
BDCCatalog(app)

with app.app_context():
    mimetypes = [
        'image/png',
        'image/tiff', 'image/tiff; application=geotiff',
        'image/tiff; application=geotiff; profile=cloud-optimized',
        'text/plain',
        'text/html',
        'application/json',
        'application/geo+json',
        'application/x-tar',
        'application/gzip'
    ]

    for mimetype in mimetypes:
        mime = MimeType(name=mimetype)
        mime.save()
