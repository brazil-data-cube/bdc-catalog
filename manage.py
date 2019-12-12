import os

from bdc_db import BDCDatabase
from flask import Flask
from flask_script import Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:datacube_2019@datacube-001.dpi.inpe.br:54320/bdc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

manager = Manager(app)
BDCDatabase(app)

from bdc_db.models import db
from flask_migrate import MigrateCommand
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('PORT', '5000'))
    except ValueError:
        PORT = 5000

    app.run(HOST, PORT)

if __name__ == '__main__':
    manager.run()