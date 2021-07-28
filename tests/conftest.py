#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Config test fixtures."""

import json
import subprocess
from pathlib import Path

import pkg_resources
import pytest
from flask import Flask


@pytest.fixture
def app():
    """Create and initialize BDC-Catalog extension."""
    _app = Flask(__name__)

    with _app.app_context():
        yield _app


@pytest.fixture
def json_data():
    """Load JSON data files for testing purposes."""
    json_dir = pkg_resources.resource_filename(__name__, 'data/')
    files = dict()
    for entry in Path(json_dir).rglob('*.json'):
        with entry.open():
            data = json.loads(entry.read_text())
        parent = str(entry.relative_to(json_dir))

        files[parent] = data
    return files


@pytest.fixture
def collections_data(json_data):
    """Retrieve the JSON data related with collections."""
    return {k: v for k, v in json_data.items() if k.startswith('collections/')}


@pytest.fixture
def grids_data(json_data):
    """Retrieve the JSON data related with Grids."""
    return {k: v for k, v in json_data.items() if k.startswith('grids/')}


@pytest.fixture
def composite_functions_data(json_data):
    """Retrieve the JSON data related with collections."""
    return {k: v for k, v in json_data.items() if k.startswith('composite_functions/')}


def pytest_sessionstart(session):
    """Load BDC-Catalog and prepare database environment."""
    for command in ['init', 'create-namespaces', 'create-extension-postgis', 'create-schema']:
        subprocess.call(f'bdc-catalog db {command}', shell=True)


def pytest_sessionfinish(session, exitstatus):
    """Destroy database created."""
    subprocess.call(f'bdc-catalog db destroy --force', shell=True)
