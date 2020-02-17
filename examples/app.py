from flask import Flask

from bdc_db import BDCDatabase

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bdc_db'

BDCDatabase(app)
