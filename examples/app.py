from bdc_db import BDCDatabase
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bdc_db'

BDCDatabase(app)
