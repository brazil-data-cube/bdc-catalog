from .base_sql import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class BandComposition(BaseModel):
    __tablename__ = 'band_compositions'

    # id = Column(Integer, primary_key=True, auto_increment=True)
    collection_id = Column(ForeignKey('collections.id'), primary_key=True, nullable=False)
    band_id = Column(ForeignKey('bands.id'), primary_key=True, nullable=False)
    product = Column(String(16), primary_key=True, nullable=False, unique=True)
    product_band = Column(String(16), primary_key=True, nullable=False, unique=True)
    description = Column(String(64))

    band = relationship('Band')
    collection = relationship('Collection')
