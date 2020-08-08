#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from flask import Flask
from flask_migrate import Migrate

from .cli import cli
from .models import db


class BDCCatalog:
    def __init__(self, app=None, **kwargs):
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app: Flask, **kwargs):
        db.init_app(app)
        self.migrate = Migrate(app, db, **kwargs)

        app.extensions['bdc-db'] = self
        app.cli.add_command(cli)
