#!/usr/bin/env bash
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

pydocstyle --match-dir="^bdc_catalog/alembic" bdc_catalog tests setup.py && \
isort bdc_catalog tests setup.py --check-only --diff --skip-glob "bdc_catalog/alembic/*" && \
check-manifest --ignore ".travis-*" --ignore ".readthedocs.*" && \
sphinx-build -qnW --color -b doctest docs/sphinx/ docs/sphinx/_build/doctest && \
pytest