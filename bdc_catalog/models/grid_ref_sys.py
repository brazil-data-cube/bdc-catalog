#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for table ``bdc.grid_ref_sys``."""

from typing import Dict, Iterable, Union

import geoalchemy2
from sqlalchemy import Column, Index, Integer, String, Table, Text, func, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import relationship

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel, db

Feature = Dict[str, str]


class GridRefSys(BaseModel):
    """Model for table ``bdc.grid_ref_sys``.

    A GridRefSys (GRS - Grid Reference System) ia a geographic reference system that divides
    the space into regions (TILE) and uses a code system, specified by a set of numbers,
    letters, or symbols, to identify an unique region, as defined
    in `BDC-Concepts <https://brazil-data-cube.github.io/products/specifications/concepts.html>`_.
    """

    __tablename__ = 'grid_ref_sys'
    __table_args__ = dict(
        schema=BDC_CATALOG_SCHEMA
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    table_id = Column(OID, nullable=False)

    tiles = relationship('Tile')

    @classmethod
    def create_geometry_table(cls, table_name: str, features: Iterable[Feature], srid=None, **kwargs) -> 'GridRefSys':
        """Create an table to store the features and retrieve a respective Grid instance.

        Args:
            table_name - Grid name (Used as table_name).
            features - Iterable with tile and geom mapped.
            schema - Table schema. Default is value associated in `db.metadata`.
            srid - SRID for grid. Default is Brazil Data Cube SRID.
        """
        grs = cls()
        grs.name = table_name

        if srid is None:
            srid = 100001

        db.metadata.schema = BDC_CATALOG_SCHEMA

        opts = kwargs.copy()

        grid_table = Table(
            table_name.lower(), db.metadata,
            db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
            db.Column('tile', db.String),
            db.Column('geom', geoalchemy2.Geometry(geometry_type='Polygon', srid=srid, spatial_index=False)),
            Index(None, 'geom', postgresql_using='gist'),
            **opts
        )

        if grid_table.exists(db.engine):
            raise RuntimeError(f'Table {table_name} already exists')

        grid_table.create(bind=db.engine)

        db.session.execute(grid_table.insert().values(features))

        table_id = cls.get_table_id(table_name, schema=opts.get('schema'))

        grs.table_id = table_id

        return grs

    @classmethod
    def get_table_id(cls, grs_name: str, schema=None) -> str:
        """Retrieve a Table OID from a Grid name.

        Raises:
            Exception when there is no table geometry for grid name.
        """
        if schema is None:
            schema = db.metadata.schema or 'public'

        res = db.session.execute(f'SELECT \'{schema}.{grs_name.lower()}\'::regclass::oid AS table_id').first()

        return res.table_id

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
            grs_name: The GRID name

        Returns:
            Table: A SQLAlchemy table reference to GRID geometry table.
        """
        expr = text('SELECT relname AS table_name, '
                    'relnamespace::regnamespace::text AS schema '
                    'FROM bdc.grid_ref_sys, pg_class '
                    'WHERE bdc.grid_ref_sys.table_id = pg_class.oid AND '
                    'LOWER(bdc.grid_ref_sys.name) = :table_name')
        res = db.session.execute(expr.bindparams(table_name=grs_name.lower())).fetchone()

        if res:
            return Table(res.table_name, db.metadata, schema=res.schema, autoload=True, autoload_with=db.engine)

        return None

    @property
    def geom_table(self) -> Union[Table, None]:
        """Retrieve instance GRID geometry table."""
        return self.get_geom_table(self.name)
