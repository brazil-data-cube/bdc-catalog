#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, String
from sqlalchemy.orm import relationship

from .base_sql import BaseModel


class CollectionTile(BaseModel):
    __tablename__ = 'collection_tiles'
    __table_args__ = (
        ForeignKeyConstraint(['grs_schema_id', 'tile_id'], ['tiles.grs_schema_id', 'tiles.id']),
    )
    collection_id = Column(ForeignKey('collections.id'), primary_key=True, nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), primary_key=True, nullable=False)
    tile_id = Column(String, primary_key=True, nullable=False)

    collection = relationship('Collection')
    grs_schema = relationship('GrsSchema')
    tile = relationship('Tile')