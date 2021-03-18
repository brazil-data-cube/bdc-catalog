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


@pytest.fixture
def db(app):
    ext = BDCCatalog(app)

    yield ext.db


def _prepare_grs_fields():
    features = [
        dict(tile='000000', geom=from_shape(Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]), srid=4326))
    ]
    return dict(
        table_name='FakeGrid',
        features=features
    )


def test_create_grid(db):
    fields = _prepare_grs_fields()
    with db.session.begin_nested():
        grs = GridRefSys.create_geometry_table(**fields, srid=4326, schema='public')
        db.session.add(grs)
    db.session.commit()

    assert grs and grs.name == fields['table_name']
    assert grs.geom_table is not None
    assert grs.crs == '+proj=longlat +datum=WGS84 +no_defs '

    with pytest.raises(RuntimeError) as e:
        _ = GridRefSys.create_geometry_table(**fields, srid=4326, schema='public', extend_existing=True)

    assert str(e.value) == f'Table {fields["table_name"]} already exists'
