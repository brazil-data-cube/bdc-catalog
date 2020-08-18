#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for BDC-Catalog CLI."""

import subprocess

from click.testing import CliRunner

from bdc_catalog.cli import cli


def test_basic_cli():
    """Test basic cli usage."""
    res = CliRunner().invoke(cli)

    assert res.exit_code == 0


def test_database_creation():
    """Test cli database creation."""
    exit_status = subprocess.call('bdc-catalog db create-db', shell=True)

    assert exit_status == 0


def test_fixtures_init(app):
    """Test cli fixtures init."""
    exit_status = subprocess.call('bdc-catalog fixtures init', shell=True)

    assert exit_status == 0
