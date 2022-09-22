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

"""Unit-test for models of BDC-Catalog."""

import pytest
from geoalchemy2.shape import from_shape
from shapely.geometry import Polygon

from bdc_catalog import BDCCatalog
from bdc_catalog.models import GridRefSys, MimeType


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


def test_base_query_methods(db):
    fields = _prepare_grs_fields()
    grs: GridRefSys = GridRefSys.query().filter(GridRefSys.name == fields['table_name']).first_or_404()
    grs.description = 'Description of Fake Grid'
    grs.save(commit=True)

    expected_mime_types = ('application/json', 'application/geo+json', 'image/png', 'image/jpeg', 'text/html')
    mimes = [
        MimeType(name=mime)
        for mime in expected_mime_types
    ]
    MimeType.save_all(mimes)
    db_mimes = MimeType.query().all()
    for mime in db_mimes:
        assert mime.name in expected_mime_types
