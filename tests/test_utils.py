#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for check_sum multihash generation."""

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

import multihash

from bdc_catalog.ext import BDCCatalog
from bdc_catalog.utils import multihash_checksum_sha256, validate_schema


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


def test_validate_json_schema(app):
    """Test minimal json schema validator."""
    _ = BDCCatalog(app)

    date_str = "2020-01-01T00:00:00"
    assets = dict(
        thumbnail={
            'href': 'http://fakehost/file.png',
            'type': 'image/png',
            'created': date_str,
            'updated': date_str,
            'roles': ['thumbnail'],
            'checksum:multihash': '1208abcd',
            'bdc:size': 0
        }
    )

    validate_schema('item-assets.json', assets)
