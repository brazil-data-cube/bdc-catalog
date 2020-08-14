#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from datetime import datetime

from bdc_db.db import db
from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.orm import Query
from sqlalchemy.ext.declarative import declared_attr


class CreatedUpdatedMixin:
    """Define base mixin to add `created` and `updated` fields."""

    @declared_attr
    def created(self):
        return Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    @declared_attr
    def updated(self):
        return Column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class BaseModel(db.Model, CreatedUpdatedMixin):
    __abstract__ = True

    @classmethod
    def query(cls) -> Query:
        return db.session.query(cls)

    @classmethod
    def save_all(cls, objects):
        """Save list of objects in database"""
        db.session.bulk_save_objects(objects)
        db.session.commit()

    def save(self, commit=True):
        """Save record in database

        Args:
            commit (bool) - Auto commit. Default is True
        """
        with db.session.begin_nested():
            db.session.add(self)

        if commit:
            db.session.commit()
