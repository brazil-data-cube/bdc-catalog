#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019-2020 INPE.
#
# Brazil Data Cube Database moduleis free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Config test fixtures."""

from typing import List

import pytest
from flask import Flask

from bdc_db.cli import create_app
from bdc_db.fixtures.cli import load_fixtures
from bdc_db.models import Collection, Tile, db


@pytest.fixture
def app() -> Flask:
    """Create flask app and set app_context."""
    _app = create_app()

    with _app.app_context():
        db.drop_all()
        db.create_all()

        yield app

        db.close_all_sessions()
        db.drop_all()


@pytest.fixture
def db_context(app: Flask):
    """Create database context to load fixtures."""
    load_fixtures()
    yield app


@pytest.fixture
def tiles(db_context) -> List[Tile]:
    """Retrieve all collections on database loaded from fixtures."""
    return Tile.query().filter().all()


@pytest.fixture
def collections(db_context) -> List[Collection]:
    """Retrieve all collections on database loaded from fixtures."""
    return Collection.query().filter().all()
