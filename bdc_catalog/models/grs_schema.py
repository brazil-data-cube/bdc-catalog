#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from typing import Union

from sqlalchemy import Column, Integer, String, Table, Text, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import relationship

from .base_sql import BaseModel, db


class GrsSchema(BaseModel):
    __tablename__ = 'grs_schemas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    table_id = Column(OID, nullable=False)

    __table_args__ = (
        UniqueConstraint(name),
    )

    tiles = relationship('Tile')

    @property
    def crs(self) -> Union[str, None]:
        """Retrieve the Coordinate Reference System (CRS) from the GRID."""
        spatial_ref_sys = Table('spatial_ref_sys', db.metadata, schema='public', autoload=True, autoload_with=db.engine)

        geom_table = self.geom_table

        if geom_table is None:
            return None

        res = db.session.query(spatial_ref_sys.c.proj4text)\
            .filter(spatial_ref_sys.c.srid == func.ST_SRID(geom_table.c.geom))\
            .first()

        crs = None
        if res is not None:
            crs = res.proj4text

        return crs

    @classmethod
    def get_geom_table(cls, grs_name: str) -> Union[Table, None]:
        """Retrieve the GRID geometry table based in the given grs.

        Notes:
            It does not raise error when GRID name does not exist.

        Args:
            grs_name - The GRID name

        Returns:
            Table - A SQLAlchemy table reference to GRID geometry table.
        """
        expr = text('SELECT relname AS table_name, '
                    'relnamespace::regnamespace::text AS schema '
                    'FROM bdc.grs_schemas, pg_class '
                    'WHERE bdc.grs_schemas.table_id = pg_class.oid AND '
                    'bdc.grs_schemas.name = :table_name')
        res = db.session.execute(expr.bindparams(table_name=grs_name)).fetchone()

        if res:
            return Table(res.table_name, db.metadata, schema=res.schema, autoload=True, autoload_with=db.engine)

        return None

    @property
    def geom_table(self) -> Union[Table, None]:
        """Retrieve instance GRID geometry table."""
        return self.get_geom_table(self.name)
