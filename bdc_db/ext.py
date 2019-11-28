from flask import Flask
from flask_migrate import Migrate
from bdc_db.models import db


class BDCDatabase:
    def __init__(self, app=None, **kwargs):
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app: Flask, **kwargs):
        db.init_app(app)
        self.migrate = Migrate(app, db, **kwargs)

        app.extensions['bdc-db'] = self