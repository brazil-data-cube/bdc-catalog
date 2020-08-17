#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#


def test_load_tiles(tiles):
    assert len(tiles) > 0


def test_load_database(collections):
    assert len(collections) > 0
