from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query


db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def query(cls) -> Query:
        return db.session.query(cls)

    def save(self, commit=True):
        """
        Save record in database

        Args:
            commit (bool) - Auto commit. Default is True
        """

        with db.session.begin_nested():
            db.session.add(self)

        if commit:
            db.session.commit()
