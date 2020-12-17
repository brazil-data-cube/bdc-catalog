#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Image catalog extension for Brazil Data Cube applications and services.

You can initialize this extension as following::

    from flask import Flask
    from bdc_catalog import BDCCatalog

    app = Flask(__name__)

    with app.app_context():
        ext = BDCCatalog(app)

To see all models offered by BDC-Catalog module, navigate to :exc:`bdc_catalog.models`.
"""

from .ext import BDCCatalog
from .version import __version__

__all__ = (
    'BDCCatalog',
    '__version__',
)
