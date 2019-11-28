from .base_sql import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship


class Asset(BaseModel):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    collection_id = Column(ForeignKey('collections.id'), primary_key=True, nullable=False)
    band_id = Column(ForeignKey('bands.id'), primary_key=True, nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), primary_key=True, nullable=False)
    tile_id = Column(ForeignKey('tiles.id'), primary_key=True, nullable=False)
    composite_function_id = Column(ForeignKey('composite_functions.id'))
    collection_item_id = Column(ForeignKey('collection_items.id'), primary_key=True, nullable=False, index=True)
    url = Column(Text)

    band = relationship('Band')
    composite_function = relationship('CompositeFunction')
    collection = relationship('Collection')
    collection_item = relationship('CollectionItem')
    grs_schema = relationship('GrsSchema')
    tile = relationship('Tile')
