from flask import Flask

from bdc_catalog import BDCCatalog

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bdc_db'

BDCCatalog(app)
