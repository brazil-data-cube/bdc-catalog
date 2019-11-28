from .base_sql import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class AssetComposition(BaseModel):
    __tablename__ = 'asset_compositions'

    collection_id = Column(ForeignKey('collections.id'), primary_key=True, nullable=False)
    asset = Column(Integer, primary_key=True, nullable=False)
    scene_id = Column(String(64), primary_key=True, nullable=False)
    description = Column(String(64))

    collection = relationship('Collection')