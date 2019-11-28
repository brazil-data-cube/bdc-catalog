from .base_sql import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, PrimaryKeyConstraint, String, text
from sqlalchemy.orm import relationship


class Band(BaseModel):
    __tablename__ = 'bands'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'collection_id'),
    )

    id = Column(Integer, unique=True, autoincrement=True)
    collection_id = Column(ForeignKey('collections.id'), nullable=False)
    min = Column(Float)
    max = Column(Float)
    fill = Column(Integer)
    scale = Column(String(16))
    common_name = Column(String(16))
    data_type = Column(String(16))
    mime_type = Column(String(16))
    description = Column(String(64))

    collection = relationship('Collection')