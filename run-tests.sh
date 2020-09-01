#!/usr/bin/env bash
#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

pydocstyle --match-dir="^bdc_catalog/alembic" bdc_catalog tests setup.py && \
isort bdc_catalog tests setup.py --check-only --diff --skip-glob "bdc_catalog/alembic/*" && \
check-manifest --ignore ".travis-*" --ignore ".readthedocs.*" && \
sphinx-build -qnW --color -b doctest docs/sphinx/ docs/sphinx/_build/doctest && \
pytest