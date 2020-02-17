#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def query(cls) -> Query:
        return db.session.query(cls)

    @classmethod
    def save_all(self, objects):
        """Save list of objects in database"""

        db.session.bulk_save_objects(objects)
        db.session.commit()

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
