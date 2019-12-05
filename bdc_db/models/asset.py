from .base_sql import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship


class Asset(BaseModel):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    collection_id = Column(ForeignKey('collections.id'), primary_key=True, nullable=False)
    band_id = Column(ForeignKey('bands.id'), primary_key=True, nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), primary_key=True, nullable=False)
    tile_id = Column(ForeignKey('tiles.id'), primary_key=True, nullable=False)
    collection_item_id = Column(ForeignKey('collection_items.id'), primary_key=True, nullable=False, index=True)
    url = Column(Text)
    source = Column(String(30))
    raster_size_x = Column(Float(50))
    raster_size_y = Column(Float(50))
    raster_size_t = Column(Float(50))
    chunk_size_x = Column(Float(50))
    chunk_size_y = Column(Float(50))
    chunk_size_t = Column(Float(50))

    collection = relationship('Collection')
    band = relationship('Band')
    grs_schema = relationship('GrsSchema')
    tile = relationship('Tile')
    collection_item = relationship('CollectionItem')
