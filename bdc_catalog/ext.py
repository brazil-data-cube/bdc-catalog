#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from flask import Flask

from .cli import cli


class BDCCatalog:
    def __init__(self, app=None, **kwargs):
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app: Flask, **kwargs):
        app.extensions['bdc-catalog'] = self
        app.cli.add_command(cli)
