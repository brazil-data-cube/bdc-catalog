#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Image catalog extension for Brazil Data Cube applications and services."""

from flask import Flask

from .cli import cli


class BDCCatalog:
    """Image catalog extension."""

    def __init__(self, app=None, **kwargs):
        """Initialize the catalog extension.

        Args:
            app: Flask application
            kwargs: Optional arguments (not used).
        """
        if app:
            self.init_app(app, **kwargs)


    def init_app(self, app: Flask, **kwargs):
        """Initialize Flask application instance.

        Args:
            app: Flask application
            kwargs: Optional arguments (not used).
        """
        app.extensions['bdc-catalog'] = self

        app.cli.add_command(cli)