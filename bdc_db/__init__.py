#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Database module."""

from .ext import BDCDatabase
from .version import __version__

__all__ = (
    'BDCDatabase',
    '__version__',
)
