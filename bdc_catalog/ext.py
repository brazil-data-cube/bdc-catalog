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

"""Image catalog extension for Brazil Data Cube applications and services."""

from bdc_db.ext import BrazilDataCubeDB
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .cli import cli
from .models.base_sql import db as _db


class BDCCatalog:
    """Image catalog extension.

    Examples:
        >>> from flask import Flask # doctest: +SKIP
        >>> app = Flask(__name__) # doctest: +SKIP
        >>> catalog = BDCCatalog(app) # doctest: +SKIP
        >>> db = catalog.db # doctest: +SKIP
        >>> with app.app_context(): # doctest: +SKIP
        >>>     db.session.execute('SELECT 1') # doctest: +SKIP

    When the ``BDC-Catalog`` is loaded, the module make available a command line ``bdc-catalog``
    with the following resources::

        Usage: bdc-catalog [OPTIONS] COMMAND [ARGS]...

          Database commands.

          .. note:: You can invoke more than one subcommand in one go.

        Options:
          -e, --env-file FILE   Load environment variables from this file. python-
                                dotenv must be installed.
          -A, --app IMPORT      The Flask application or factory function to load, in
                                the form 'module:name'. Module can be a dotted import
                                or file path. Name is not required if it is 'app',
                                'application', 'create_app', or 'make_app', and can be
                                'name(args)' to pass arguments.
          --debug / --no-debug  Set debug mode.
          --version             Show the Flask version.
          --help                Show this message and exit.

        Commands:
          alembic    Perform database migrations.
          db         More database commands.
          instance   Instance commands.
          lccs       More lccs database commands.
          load-data  Command line to load collections JSON into database.
          routes     Show the routes for the app.
          run        Run a development server.
          shell      Run a shell in the app context.

    You may proceed to the :doc:`cli` to see all supported command lines.
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
