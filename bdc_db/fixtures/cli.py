#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019-2020 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Python Brazil Data Cube Database Fixture click client."""

from json import loads as json_parser

from bdc_db.models import db, Asset, Band, Collection, CollectionItem, CollectionTile, CompositeFunctionSchema, GrsSchema, Tile
from flask.cli import with_appcontext
from pkg_resources import resource_string
import click


@click.group(chain=True)
def fixtures():
    """Command for loading Brazil Data Cube Datababase data."""


@fixtures.command()
@with_appcontext
def init():
    """Initialize default fixtures."""
    load_fixtures()


def load_model(fixture_path: str, model_class):
    """Load fixture to database.

    Args:
        fixture_path - Path relative to fixtures. i.e 'data/tiles.json'
        model_class - SQLAlchemy Model Class
    """
    schemas = json_parser(resource_string(__name__, fixture_path))

    with db.session.begin_nested():
        for schema in schemas:
            model = model_class(**schema)

            model.save(commit=False)


def load_collections(fixture_path: str):
    """Load default collections to database.

    Args:
        fixture_path - Path relative to fixtures. i.e 'data/tiles.json'
    """
    collections = json_parser(resource_string(__name__, fixture_path))

    with db.session.begin_nested():
        for collection in collections:
            bands = collection.pop('bands')

            c = Collection(**collection)
            c.save(commit=False)

            for band in bands:
                b = Band(**band)
                b.collection = c

                b.save(commit=False)


def load_items(fixture_path: str):
    """Load default items and assets to database.

    Args:
        fixture_path - Path relative to fixtures. i.e 'data/items.json'
    """
    items = json_parser(resource_string(__name__, fixture_path))

    with db.session.begin_nested():
        for item in items:
            assets = item.pop('assets')

            c_item = CollectionItem(**item)
            c_item.save(commit=False)

            c_tile = CollectionTile()
            c_tile.collection_id = c_item.collection_id
            c_tile.grs_schema_id = c_item.grs_schema_id
            c_tile.tile_id = c_item.tile_id
            c_tile.save(commit=False)

            for asset in assets:
                b = Band.query().filter(
                    Band.collection_id == c_item.collection_id,
                    Band.name == asset.pop('band')
                ).one()

                a = Asset(**asset)
                a.band = b

                a.save(commit=False)


def load_fixtures():
    """Load default database fixtures."""
    load_model('data/grs_schemas.json', GrsSchema)
    load_model('data/tiles.json', Tile)
    load_model('data/composite_functions.json', CompositeFunctionSchema)
    load_collections('data/collections.json')
    load_items('data/items.json')

    db.session.commit()