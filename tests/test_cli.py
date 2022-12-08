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

"""Unit-test for BDC-Catalog CLI."""

import subprocess
import sys

import pytest
from click import MissingParameter
from click.testing import CliRunner

from bdc_catalog.cli import cli, load_data


def test_basic_cli():
    """Test basic cli usage."""
    res = CliRunner().invoke(cli)

    assert res.exit_code == 0


def test_cli_module():
    """Test the BDCCatalog invoked as a module."""
    res = subprocess.call(f'{sys.executable} -m bdc_catalog', shell=True)

    assert res == 0


def test_cli_load_data(fixture_dir):
    """Test the BDCCatalog invoked as a module."""
    # Test missing parameter
    res = CliRunner().invoke(load_data, args=[])
    assert res.exit_code != 0
    assert "Missing --ifile or --from-dir parameter" in res.output

    res = CliRunner().invoke(load_data, args=["--from-dir", fixture_dir])
    assert res.exit_code == 0
