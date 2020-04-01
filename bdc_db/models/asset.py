#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import (and_, cast, Column, Float, ForeignKey, ForeignKeyConstraint,
                        func, Index, Integer, select, String, Text, text)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import create_materialized_view

from .band import Band
from .base_sql import BaseModel
from .collection_item import CollectionItem


class Asset(BaseModel):
    __tablename__ = 'assets'
    __table_args__ = (
        ForeignKeyConstraint(['grs_schema_id', 'tile_id'], ['tiles.grs_schema_id', 'tiles.id']),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, server_default=text("nextval('assets_id_seq'::regclass)"))
    collection_id = Column(ForeignKey('collections.id'), nullable=False)
    band_id = Column(ForeignKey('bands.id'), primary_key=True, nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), primary_key=True, nullable=False)
    tile_id = Column(String, primary_key=True, nullable=False)
    collection_item_id = Column(ForeignKey('collection_items.id'), primary_key=True, nullable=False, index=True)
    url = Column(Text)
    source = Column(String(30))
    raster_size_x = Column(Float(53))
    raster_size_y = Column(Float(53))
    raster_size_t = Column(Float(53))
    chunk_size_x = Column(Float(53))
    chunk_size_y = Column(Float(53))
    chunk_size_t = Column(Float(53))

    collection = relationship('Collection')
    band = relationship('Band')
    grs_schema = relationship('GrsSchema')
    tile = relationship('Tile')
    collection_item = relationship('CollectionItem')


class AssetMV(BaseModel):
    __tablename__ = 'assets_mv'
    _x = select([CollectionItem.id.label('item_id'),
                            Band.common_name.label('band'),
                            func.json_build_object('href', Asset.url).label('url')
                           ]).where(and_(Asset.collection_item_id == CollectionItem.id,
                                     Asset.band_id == Band.id)).alias('x')
    __table__ = create_materialized_view(name=__tablename__,
        selectable=select([_x.c.item_id, cast(func.json_object_agg(_x.c.band, _x.c.url), JSONB).op('||')(
                          cast(func.json_build_object('thumbnail',
                               func.json_build_object('href', CollectionItem.quicklook)),
                               JSONB)).label('asset')]).
        select_from(_x).
        where(CollectionItem.id == _x.c.item_id).
        group_by(_x.c.item_id, CollectionItem.quicklook),
        metadata=BaseModel.metadata,
        indexes=[Index(f'idx_{__tablename__}_item_id', 'item_id')]
    )
