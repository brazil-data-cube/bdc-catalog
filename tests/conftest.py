#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019-2020 INPE.
#
# Brazil Data Cube Database moduleis free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Config test fixtures."""

from json import loads as json_parser
from typing import List
from bdc_db.models import db, Band, Collection, CompositeFunctionSchema, GrsSchema, Tile
from flask import Flask
from pkg_resources import resource_string
import pytest

from bdc_db.cli import create_app


def load_model(fixture_path: str, model_class):
    """Load fixture to database.

    Args:
        fixture_path - Path relative to fixtures. i.e 'data/tiles.json'
        model_class - SQLAlchemy Model Class
    """
    schemas = json_parser(resource_string(__name__, fixture_path))

    with db.session.begin_nested():
        for schema in schemas:
            model = model_class(**schema)

            model.save(commit=False)


def load_collections(fixture_path: str):
    """Load default collections to database.

    Args:
        fixture_path - Path relative to fixtures. i.e 'data/tiles.json'
    """
    collections = json_parser(resource_string(__name__, fixture_path))

    with db.session.begin_nested():
        for collection in collections:
            bands = collection.pop('bands')

            c = Collection(**collection)
            c.save(commit=False)

            for band in bands:
                b = Band(**band)
                b.collection = c

                b.save(commit=False)


def load_fixtures():
    """Load default database fixtures."""
    load_model('data/grs_schemas.json', GrsSchema)
    load_model('data/tiles.json', Tile)
    load_model('data/composite_functions.json', CompositeFunctionSchema)
    load_collections('data/collections.json')

    db.session.commit()


@pytest.fixture
def app() -> Flask:
    _app = create_app()

    with _app.app_context():
        db.drop_all()
        db.create_all()

        # Initialize Fixtures
        load_fixtures()

        yield _app

        db.session.close_all()
        db.drop_all()


@pytest.fixture
def tiles(app: Flask) -> List[Tile]:
    """Retrieve all collections on database loaded from fixtures."""
    return Tile.query().filter().all()


@pytest.fixture
def collections(app: Flask) -> List[Collection]:
    """Retrieve all collections on database loaded from fixtures."""
    return Collection.query().filter().all()
