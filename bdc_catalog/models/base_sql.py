#
# This file is part of BDC-Catalog.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
"""Base classes for SQLAlchemy database models in BDC-Catalog."""

from datetime import datetime

from bdc_db.db import db
from sqlalchemy import TIMESTAMP, Column, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Query


class TimestampMixin:
    """Base timestamp model mixin to add the ``created`` and ``updated`` fields."""

    @declared_attr
    def created(self):
        """Define a special declarative member to record the creation of a table row."""
        return Column(TIMESTAMP(timezone=True), default=datetime.utcnow, server_default=func.now(),
                      nullable=False)

    @declared_attr
    def updated(self):
        """Define a special declarative member to record the update of a table row."""
        return Column(TIMESTAMP(timezone=True), default=datetime.utcnow, server_default=func.now(),
                      nullable=False)


class BaseModel(db.Model, TimestampMixin):
    """Base model class for BDC-Catalog classes."""

    __abstract__ = True

    @classmethod
    def query(cls) -> Query:
        """Return a query object according to the class model."""
        return db.session.query(cls)

    @classmethod
    def save_all(cls, objects):
        """Save list of objects in database."""
        db.session.bulk_save_objects(objects)
        db.session.commit()

    def save(self, commit=True):
        """Save record in database.

        Args:
            commit (bool): Auto commit. Default is True
        """
        with db.session.begin_nested():
            db.session.add(self)

        if commit:
            db.session.commit()