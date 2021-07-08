#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Utility for Image Catalog Extension."""

import hashlib
from io import BytesIO
from pathlib import Path
from typing import Any, Union

import jsonschema
import multihash as _multihash
from flask import current_app


def check_sum(file_path: Union[str, BytesIO], chunk_size=16384) -> bytes:
    """Read a file and generate a checksum using `sha256`.

    Raises:
        IOError when could not open given file.

    Args:
        file_path (str|BytesIo): Path to the file
        chunk_size (int): Size in bytes to read per iteration. Default is 16384 (16KB).

    Returns:
        The digest value in bytes.
    """
    algorithm = hashlib.sha256()

    def _read(stream):
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            algorithm.update(chunk)

    if isinstance(file_path, str) or isinstance(file_path, Path):
        with open(str(file_path), "rb") as f:
            _read(f)
    else:
        _read(file_path)

    return algorithm.digest()


def multihash_checksum_sha256(file_path: Union[str, BytesIO]):
    """Generate the checksum multihash.

    This method follows the spec `multihash <https://github.com/multiformats/multihash>`_.
    We use `sha256` as described in ``check_sum``. The multihash spec defines the code `0x12` for `sha256` and
    must have `0x20` (32 chars) length.

    See more in https://github.com/multiformats/py-multihash/blob/master/multihash/constants.py#L4

    Args:
        file_path (str|BytesIo): Path to the file

    Returns:
        A string-like hash in hex-decimal
    """
    sha256 = 0x12
    sha256_length = 0x20

    _hash = _multihash.encode(digest=check_sum(file_path), code=sha256, length=sha256_length)

    return _multihash.to_hex_string(_hash)


def validate_schema(schema_key: str, value: Any, draft_checker=jsonschema.draft7_format_checker) -> Any:
    """Validate a JSONSchema according a json model.

    Note:
        This method works under a Flask Application Context since it seeks for JSONSchema
        loaded into :func:`~bdc_catalog.ext.BDCCatalog`

    Args:
        schema_key (str): The schema key path reference to the `jsonschemas` folder.
        value (Any): The model value to be validated.
        draft_checker (jsonschema.FormatChecker): The format checker validation for schemas.
    """
    extension = current_app.extensions['bdc-catalog']

    schema = extension.schemas.get_schema(schema_key)
    jsonschema.validate(instance=value, schema=schema, format_checker=draft_checker)

    return value
