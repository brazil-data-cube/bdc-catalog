#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Image catalog extension for Brazil Data Cube applications and services."""

from bdc_db.ext import BrazilDataCubeDB
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .cli import cli
from .models.base_sql import db as _db


class BDCCatalog:
    """Image catalog extension.

    Examples:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> catalog = BDCCatalog(app)
        >>> # db Flask-SQLAlchemy instance
        >>> db = catalog.db
        >>> with app.app_context():
        >>>     db.session.execute('SELECT 1')
    """

    # Reference to BrazilDataCubeDB app instance
    _db_ext = None

    def __init__(self, app=None):
        """Initialize the catalog extension.

        Args:
            app: Flask application
        """
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialize Flask application instance.

        Args:
            app: Flask application
        """
        self._db_ext = BrazilDataCubeDB(app)
        app.extensions['bdc-catalog'] = self

        app.cli.add_command(cli)

    @property
    def db(self) -> SQLAlchemy:
        """Retrieve instance Flask-SQLALchemy instance.

        Notes:
            Make sure to initialize the `BDCCatalog` before.
        """
        return _db
