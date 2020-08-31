#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for check_sum multihash generation."""

from pathlib import Path
from tempfile import TemporaryDirectory

import multihash

from bdc_catalog.utils import multihash_checksum_sha256


def test_check_sum_sha256():
    """Test basic check_sum multihash generation."""
    with TemporaryDirectory() as tmp:
        tmp_file = Path(tmp) / 'file.txt'
        with open(tmp_file, 'w') as f:
            f.write('Testing')

        _hash = multihash_checksum_sha256(tmp_file)

        assert _hash == '1220e806a291cfc3e61f83b98d344ee57e3e8933cccece4fb45e1481f1f560e70eb1'

        digest = multihash.from_hex_string(_hash)

        # Ensure digest is a multihash
        assert multihash.is_valid(digest)
