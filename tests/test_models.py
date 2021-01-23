#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for models of BDC-Catalog."""

import pytest
from geoalchemy2.shape import from_shape
from shapely.geometry import Polygon

from bdc_catalog import BDCCatalog
from bdc_catalog.models import GridRefSys


@pytest.fixture(scope='session')
def db(app):
    ext = BDCCatalog(app)

    yield ext.db


def test_create_grid(db):
    features = [
        dict(tile='000000', geom=Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]))
    ]

    grs_name = 'FakeGrid'
    with db.session.begin_nested:
        grs = GridRefSys.create_geometry_table(grs_name, features=features, srid=4326)
    db.session.commit()

    assert grs
