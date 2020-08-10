#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os

import click
from flask import Flask
from flask.cli import FlaskGroup, with_appcontext
from flask_migrate.cli import db as flask_migrate_db
from sqlalchemy_utils.functions import create_database, database_exists

from .fixtures.cli import fixtures
from .models import db


def create_app():
    from .ext import BDCCatalog

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                                           'postgresql://postgres:postgres@localhost:5432/bdcdb')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    BDCCatalog(app)

    return app


def create_cli(create_app=None):
    """
    Wrapper creation of Flask App in order to attach into flask click

    Args:
         create_app (function) - Create app factory (Flask)
    """
    def create_cli_app(info):
        if create_app is None:
            info.create_app = None

            app = info.load_app()
        else:
            app = create_app()

        return app

    @click.group(cls=FlaskGroup, create_app=create_cli_app)
    def cli(**params):
        """Command line interface for bdc_collection_builder"""
        pass

    return cli


cli = create_cli(create_app=create_app)
cli.add_command(fixtures)


@flask_migrate_db.command()
@with_appcontext
def create_db():
    """Create database. Make sure the variable SQLALCHEMY_DATABASE_URI is set"""
    click.secho('Creating database {0}'.format(db.engine.url),
                fg='green')
    if not database_exists(str(db.engine.url)):
        create_database(str(db.engine.url))

    click.secho('Creating extension postgis...', fg='green')
    with db.session.begin_nested():
        db.session.execute('CREATE EXTENSION IF NOT EXISTS postgis')

    db.session.commit()



def main(as_module=False):
    # TODO omit sys.argv once https://github.com/pallets/click/issues/536 is fixed
    import sys
    cli.main(args=sys.argv[1:], prog_name="python -m bdc_db" if as_module else None)