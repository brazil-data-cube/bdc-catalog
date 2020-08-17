#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Database module."""

from .ext import BDCCatalog
from .version import __version__

__all__ = (
    'BDCCatalog',
    '__version__',
)
