#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Represent the custom data types for BDC-Catalog."""

from typing import Any

from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB

from .utils import validate_schema


class JSONSchemaType(TypeDecorator):
    """Custom Data Type for dealing with JSONB and JSONSchemas on SQLAlchemy."""

    _schema_key: str
    _draft_checker: Any
    impl = JSONB

    def __init__(self, schema: str, draft_checker=None, *args, **kwargs):
        """Build a new data type."""
        self._schema_key = schema
        self._draft_checker = draft_checker
        super().__init__(*args, **kwargs)

    def coerce_compared_value(self, op, value):
        """Define a 'coerced' Python value in an expression.

        Note:
            Implements native SQLAlchemy :class:`~sqlalchemy.dialects.postgresql.JSONB`.
        """
        return self.impl.coerce_compared_value(op, value)

    def process_bind_param(self, value, dialect):
        """Apply JSONSchema validation and bind the JSON value to the SQLAlchemy Engine execution."""
        options = dict()
        if self._draft_checker:
            options['draft_checker'] = self._draft_checker
        if value is not None:
            validate_schema(self._schema_key, value, **options)

        return value
