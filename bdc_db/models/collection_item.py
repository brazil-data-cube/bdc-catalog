#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import (Column, Date, Float, ForeignKey, ForeignKeyConstraint,
                        String, Text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base_sql import BaseModel


class CollectionItem(BaseModel):
    __tablename__ = 'collection_items'
    __table_args__ = (
        ForeignKeyConstraint(['grs_schema_id', 'tile_id'], ['tiles.grs_schema_id', 'tiles.id']),
    )

    id = Column(String, primary_key=True, nullable=False, unique=True)
    collection_id = Column(ForeignKey('collections.id'), primary_key=True, nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), primary_key=True, nullable=False)
    tile_id = Column(String, primary_key=True, nullable=False)
    item_date = Column(Date, primary_key=True, nullable=False)
    composite_start = Column(Date, nullable=False, index=True)
    composite_end = Column(Date, index=True)
    quicklook = Column(Text)
    cloud_cover = Column(Float)
    scene_type = Column(String)
    compressed_file = Column(String)
    assets_json = Column(JSONB)

    cube_collection = relationship('Collection')
    grs_schema = relationship('GrsSchema')
    tile = relationship('Tile')
