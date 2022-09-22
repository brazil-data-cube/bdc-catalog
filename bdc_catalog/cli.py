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

"""Command-Line Interface for BDC-Catalog."""

import json
from pathlib import Path

import click
from bdc_db.cli import cli

from bdc_catalog.models import Item
from bdc_catalog.utils import create_collection, create_item

try:
    import shapely.geometry
except ImportError:
    shapely = None


@cli.command()
@click.option('-i', '--ifile', type=click.Path(exists=True, file_okay=True, readable=True))
@click.option('--from-dir', type=click.Path(exists=True, dir_okay=True, readable=True))
@click.option('-v', '--verbose', is_flag=True, default=False)
def load_data(ifile: str, from_dir: str, verbose: bool):
    """Command line to load collections and Items JSON into database.

    Note:
        Make sure you have exported variable ``SQLALCHEMY_DATABASE_URI`` before
        like ``SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost/bdc``.

    Note:
        It skips collection that already exists.
        You must give at least ``--ifile`` or ``--from_dir`` parameter.

    To load a single file JSON collection, use parameter ``-i`` or verbose ``--ifile path/to/json``::

        bdc-catalog load-data --ifile examples/fixtures/sentinel-2.json -v

    The following output will be displayed::

        Collection S2_L1C-1 created
        -> Creating Item S2A_MSIL1C_20151122T132122_N0204_R038_T23LMF_20151122T132134
        - Total 1 items created.

    If you would like to read a directory containing several JSON collection files::

        bdc-catalog load-data --from-dir examples/fixtures

    Args:
        ifile (str): Path to JSON file. Default is ``None``.
        from_dir (str): Readable directory containing JSON files. Defaults to ``None``.
        verbose (bool): Display verbose output. Defaults to ``False``.
    """
    if shapely is None:
        raise ImportError('This command line requires "shapely" installed.'
                          'Make sure to install with "pip install shapely" or '
                          '"pip install -e .[geo]".')

    entries = []
    if ifile:
        entries.append(Path(ifile))
    elif from_dir:
        for entry in Path(from_dir).glob('*.json'):
            entries.append(entry)
    else:
        raise click.MissingParameter("Missing --ifile or --from-dir parameter.")

    for entry in entries:
        with entry.open() as fd:
            data = json.load(fd)

        items = data.pop('items', [])
        collection, created = create_collection(**data)
        msg = 'created' if created else 'skipped.'
        click.secho(f'Collection {collection.name}-{collection.version} {msg}', fg='green', bold=True)
        affected_items = 0
        for item in items:
            name = item.get('name')
            item_ref = Item.query().filter(Item.collection_id == collection.id, Item.name == name).first()
            if item_ref is None:
                bbox = item.get('bbox')
                footprint = item.get('footprint')
                if bbox:
                    item['bbox'] = shapely.geometry.shape(bbox)
                    item['footprint'] = shapely.geometry.shape(footprint)

                item_ref = create_item(collection_id=collection.id, **item)
                affected_items += 1
                if verbose:
                    click.secho(f'-> Creating Item {item_ref.name}')
        click.secho(f'- Total {affected_items} items created.')


def main(as_module=False):
    """Run run the library module as a script."""
    # TODO omit sys.argv once https://github.com/pallets/click/issues/536 is fixed
    import sys
    cli.main(args=sys.argv[1:], prog_name="python -m bdc_catalog" if as_module else None)
