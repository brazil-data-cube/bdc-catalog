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

"""Unit-test for check_sum multihash generation."""

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

import multihash
from geoalchemy2.elements import WKBElement
from shapely.geometry import Polygon

from bdc_catalog.utils import geom_to_wkb, multihash_checksum_sha256


def test_check_sum_sha256():
    """Test basic check_sum multihash generation."""
    with TemporaryDirectory() as tmp:
        tmp_file = Path(tmp) / 'file.txt'
        message = 'Testing'
        with open(tmp_file, 'w') as f:
            f.write(message)

        _hash = multihash_checksum_sha256(tmp_file)

        expected_hash = '1220e806a291cfc3e61f83b98d344ee57e3e8933cccece4fb45e1481f1f560e70eb1'

        assert _hash == expected_hash
        # Try using stream instead file
        stream = BytesIO(message.encode())
        stream_hash = multihash_checksum_sha256(stream)
        assert stream_hash == expected_hash

        digest = multihash.from_hex_string(_hash)

        # Ensure digest is a multihash
        assert multihash.is_valid(digest)


def test_geom_to_wkb():
    """Test the creation of EWKB geometries and if the values are kept."""
    geom = Polygon([
        (2609666.347361833, 11854042.174822256),
        (2777726.39537163, 11854042.174822256),
        (2777726.39537163, 11963904.01588614),
        (2609666.347361833, 11963904.01588614),
        (2609666.347361833, 11854042.174822256),
    ])
    srid = 100001
    wkb = geom_to_wkb(geom, srid=srid)
    assert isinstance(wkb, WKBElement)
    assert wkb.srid == srid
