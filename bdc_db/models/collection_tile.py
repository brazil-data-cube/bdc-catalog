from .base_sql import BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class CollectionTile(BaseModel):
    __tablename__ = 'collection_tiles'

    collection_id = Column(ForeignKey('collections.id'), primary_key=True, nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), primary_key=True, nullable=False)
    tile_id = Column(ForeignKey('tiles.id'), primary_key=True, nullable=False)

    collection = relationship('Collection')
    grs_schema = relationship('GrsSchema')
    tile = relationship('Tile')