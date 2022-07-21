#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Config test fixtures."""

import subprocess

import pytest
from flask import Flask


@pytest.fixture
def app():
    """Create and initialize BDC-Catalog extension."""
    _app = Flask(__name__)

    with _app.app_context():
        yield _app


def pytest_sessionstart(session):
    """Load BDC-Catalog and prepare database environment."""
    for command in ['init', 'create-namespaces', 'create-extension-postgis']:
        subprocess.call(f'bdc-catalog db {command}', shell=True)

    subprocess.call(f'lccs-db db create-extension-hstore', shell=True)
    # Create tables
    subprocess.call(f'bdc-catalog db create-schema', shell=True)


def pytest_sessionfinish(session, exitstatus):
    """Destroy database created."""
    subprocess.call(f'bdc-catalog db destroy --force', shell=True)
