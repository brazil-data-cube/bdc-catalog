from .base_sql import BaseModel
from sqlalchemy import Column, Date, ForeignKey, String, Text
from sqlalchemy.orm import relationship


class CollectionItem(BaseModel):
    __tablename__ = 'collection_items'

    id = Column(String(64), primary_key=True, nullable=False, unique=True)
    collection_id = Column(ForeignKey('collections.id'), primary_key=True, nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), primary_key=True, nullable=False)
    tile_id = Column(ForeignKey('tiles.id'), primary_key=True, nullable=False)
    composite_function_id = Column(ForeignKey('composite_functions.id'), primary_key=True, nullable=False)
    item_date = Column(Date, primary_key=True, nullable=False)
    composite_start = Column(Date, nullable=False, index=True)
    composite_end = Column(Date, index=True)
    quicklook = Column(Text)

    composite_function = relationship('CompositeFunction')
    cube_collection = relationship('CubeCollection')
    grs_schema = relationship('GrsSchema')
    tile = relationship('Tile')