#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for models of BDC-Catalog."""
from datetime import datetime

import pyproj
import pytest
from geoalchemy2.shape import from_shape
from shapely.geometry import shape

from bdc_catalog import BDCCatalog
from bdc_catalog.models import (Band, Collection, CompositeFunction,
                                GridRefSys, Item, SpatialRefSys)


@pytest.fixture
def db(app):
    ext = BDCCatalog(app)

    yield ext.db


COLLECTION_NAME = 'FakeCollection'
COLLECTION_VERSION = 1


def _adapt_features(features, srid):
    out = [
        dict(tile=feature['tile'], geom=from_shape(shape(feature['geom']), srid=srid))
        for feature in features
    ]

    return out


def _get_collection():
    return Collection.query()\
        .filter(Collection.name == COLLECTION_NAME, Collection.version == str(COLLECTION_VERSION)) \
        .first_or_404()


def test_base_model_save(db):
    """Test a simple collection creation, before and after commit."""
    collection = Collection()
    collection.name = COLLECTION_NAME
    collection.version = COLLECTION_VERSION
    collection.is_public = False
    collection.collection_type = 'collection'
    collection.title = f'The title of {collection.name}'
    collection._metadata = dict(
        platform=dict(
            instruments=['MSI']
        )
    )
    collection.save(commit=False)

    assert collection in db.session

    collection.save(commit=True)

    assert collection.id is not None


def test_base_model_bulk_create(db):
    """Test the bulk object creation using bdc-catalog utility."""
    collection = _get_collection()

    items = []
    now = datetime.now()
    for i in range(1, 11):
        item = Item()
        item.collection_id = collection.id
        item.name = f'Scene_{i}'
        item.start_date = item.end_date = now
        items.append(item)

    Item.save_all(items)

    expected = Item.query().filter(Item.collection_id == collection.id).all()
    assert len(expected) == len(items)


def test_create_grid(db, grids_data):
    """Test the creation of Grids."""
    for file_name, data in grids_data.items():
        proj4 = data.pop('proj', None)
        srid = data['srid']
        data['features'] = _adapt_features(data['features'], srid)

        with db.session.begin_nested():
            spatial_ref_sys = db.session.query(SpatialRefSys).filter_by(srid=srid).first()
            if spatial_ref_sys is None:
                crs = pyproj.CRS.from_proj4(proj4)
                spatial_ref_sys = SpatialRefSys(
                    auth_name='Albers Equal Area',
                    auth_srid=srid,
                    srid=srid,
                    srtext=crs.to_wkt(),
                    proj4text=proj4
                )
                db.session.add(spatial_ref_sys)
            else:
                crs = pyproj.CRS.from_epsg(srid)

            grs = GridRefSys.create_geometry_table(**data, schema='public')
            db.session.add(grs)
        db.session.commit()

        assert grs and grs.name == data['table_name']
        assert grs.geom_table is not None

        # TODO: Remove this check and make right validation using pyproj version in to_proj4 function.
        assert grs.crs in crs.to_proj4()

        with pytest.raises(RuntimeError) as e:
            _ = GridRefSys.create_geometry_table(**data, schema='public', extend_existing=True)

        assert str(e.value) == f'Table {data["table_name"]} already exists'


def test_create_composite_functions(db, composite_functions_data):
    """Test the creation of pre-defined composite functions."""
    for file_name, data in composite_functions_data.items():
        with db.session.begin_nested():
            composite = CompositeFunction(**data)
            db.session.add(composite)
        db.session.commit()

        assert composite.id
        assert composite.name == data['name']


def test_create_collections_models(db, collections_data):
    """Test the creation of collections, cubes."""
    for file_name, data in collections_data.items():
        if not data:
            continue

        metadata = data.pop('metadata', None)
        bands = data.pop('bands', [])
        items = data.pop('items', [])
        grid_name = data.pop('grid_ref_sys', None)
        function_name = data.pop('composition_function', None)
        _ = data.pop('quicklook', None)

        grid_id = None
        function_id = None
        if grid_name is not None:
            grid = GridRefSys.query().filter(GridRefSys.name == grid_name).first_or_404('Grid {} not found.')
            grid_id = grid.id
        if function_name is not None:
            composite_function = CompositeFunction.query().filter(CompositeFunction.name == function_name).first_or_404()
            function_id = composite_function.id

        collection = Collection(**data)
        collection.grid_ref_sys_id = grid_id
        collection.composite_function_id = function_id
        collection._metadata = metadata

        collection.save()

        if function_name:
            assert collection.composite_function.name == function_name

        for band_dict in bands:
            band_meta = band_dict.pop('metadata', None)
            _ = band_dict.pop('mime_type', None)
            _ = band_dict.pop('resolution_unit', None)

            band = Band(**band_dict)
            band._metadata = band_meta
            band.collection_id = collection.id
            band.save()

        bands_db = Band.query().filter(Band.collection_id == collection.id).all()
        assert len(bands_db) == len(bands)

        for item_dict in items:
            item = Item(**item_dict)
            item.collection_id = collection.id

            item.save()

        items_db = Item.query().filter(Item.collection_id == collection.id).all()
        assert len(items_db) == len(items)
