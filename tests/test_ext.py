#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for extension BDC-Catalog."""

from bdc_catalog import BDCCatalog


def test_ext_creation(app):
    ext = BDCCatalog(app)

    assert app.extensions['bdc-catalog'] == ext
