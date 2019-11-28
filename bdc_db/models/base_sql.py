from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query


db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def query(cls) -> Query:
        return db.session.query(cls)