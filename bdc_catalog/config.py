#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Configuration file for BDC-Catalog."""

BDC_CATALOG_SCHEMA = 'bdc'
"""Define the database schema prefix for BDC-Catalog models.

TODO: Get it as environment variable. We should take care of migrations schema before do it.
      Check the issue https://github.com/brazil-data-cube/bdc-catalog/issues/123
"""
