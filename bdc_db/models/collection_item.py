from .base_sql import BaseModel
from sqlalchemy import Column, Date, ForeignKey, String, Text, Float
from sqlalchemy.orm import relationship


class CollectionItem(BaseModel):
    __tablename__ = 'collection_items'

    id = Column(String, primary_key=True, nullable=False, unique=True)
    collection_id = Column(ForeignKey('collections.id'), primary_key=True, nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), primary_key=True, nullable=False)
    tile_id = Column(ForeignKey('tiles.id'), primary_key=True, nullable=False)
    item_date = Column(Date, primary_key=True, nullable=False)
    composite_start = Column(Date, nullable=False, index=True)
    composite_end = Column(Date, index=True)
    quicklook = Column(Text)
    cloud_cover = Column(Float)
    scene_type = Column(String)
    compressed_file = Column(String)

    cube_collection = relationship('Collection')
    grs_schema = relationship('GrsSchema')
    tile = relationship('Tile')