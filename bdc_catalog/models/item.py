#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for the image item of a collection."""

from geoalchemy2 import Geometry
from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Index, Integer, Numeric,
                        String, UniqueConstraint)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel, db
from .collection import Collection


class SpatialRefSys(db.Model):
    """Auxiliary model for the PostGIS spatial_ref_sys table."""

    __tablename__ = 'spatial_ref_sys'
    __table_args__ = ({"schema": "public"})

    srid = Column(Integer, primary_key=True)
    auth_name = Column(String)
    auth_srid = Column(Integer)
    srtext = Column(String)
    proj4text = Column(String)


class Item(BaseModel):
    """Model for the image item of a collection.

    An item is usually defined in Brazil Data Cube concept as a data product scene.

    The assets property follows the JSONSchema spec defined in :exc:`bdc_catalog.jsonschemas.item.assets.json`,
    which uses the function :meth:`bdc_catalog.utils.multihash_checksum_sha256` to generate the file checksum.

    The following example describes an published item of a Sentinel-2 data product scene ``S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053``::

        {
            "id": 423658,
            "name": "S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053",
            "collection_id": 23, # Collection S2_L1C
            "start_date": "2019-10-18T13:42:11",
            "end_date": "2019-10-18T13:42:11",
            "geom": POLYGON((-50.094208 -7.23638395134798,-49.099884 -7.23332135700407,-49.09546 -8.22598479222442,-50.09207 -8.22947294680053,-50.094208 -7.23638395134798))",
            "bbox": "POLYGON((-49.09545 -8.225985,-49.099896 -7.233321,-50.094195 -7.236384,-50.092074 -8.229473,-49.09545 -8.225985))",
            "srid": 4326,
            "assets": {
                "thumbnail": {
                    "href": "/Repository/Archive/S2_L1C/v001/22/M/FS/2019/S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053/S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053.png",
                    "type": "image/png",
                    "roles": [
                        "thumbnail"
                    ],
                    "created": "2020-12-16T18:50:05",
                    "updated": "2020-12-16T18:50:05",
                    "bdc:size": 183439,
                    "checksum:multihash": "1220476cf4b62525f99e9891634acdd3c4fbfc151e407e762ee8b32ce7ba72824a41"
                },
                "asset": {
                    "href": "/Repository/Archive/S2_L1C/v001/22/M/FS/2019/S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053/S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053.zip",
                    "type": "application/zip",
                    "roles": [
                        "data"
                    ],
                    "created": "2020-12-16T18:50:05",
                    "updated": "2020-12-16T18:50:05",
                    "bdc:size": 789501813,
                    "checksum:multihash": "1220f1cebeff261104a35b7ce68083777cf3449a733acf240120ccf949d5c758e31a"
                }
            }
        }
    """

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    collection_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.collections.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    tile_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.tiles.id', onupdate='CASCADE', ondelete='CASCADE'))
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    cloud_cover = Column(Numeric)
    assets = Column(JSONB, comment='Follow the JSONSchema @jsonschemas/item-assets.json')
    _metadata = Column('metadata', JSONB, comment='Follow the JSONSchema @jsonschemas/item-metadata.json')
    provider_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.providers.id', onupdate='CASCADE', ondelete='CASCADE'))
    application_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.applications.id', onupdate='CASCADE', ondelete='CASCADE'))
    geom = Column(Geometry(geometry_type='Polygon', srid=4326, spatial_index=False))
    bbox = Column(Geometry(geometry_type='Polygon', srid=4326, spatial_index=False))
    srid = Column(Integer, ForeignKey('public.spatial_ref_sys.srid', onupdate='CASCADE', ondelete='CASCADE'))
    properties = Column('properties', JSONB, comment='Contains the properties offered by STAC Items')

    collection = relationship(Collection)
    tile = relationship('Tile')
    provider = relationship('Provider')
    application = relationship('Application')

    __table_args__ = (
        UniqueConstraint(name, collection_id),
        Index(None, cloud_cover),
        Index(None, collection_id),
        Index(None, geom, postgresql_using='gist'),
        Index(None, bbox, postgresql_using='gist'),
        Index(None, name),
        Index(None, provider_id),
        Index('idx_items_start_date_end_date', start_date, end_date),
        Index(None, tile_id),
        Index(None, start_date.desc()),
        Index(None, application_id),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
