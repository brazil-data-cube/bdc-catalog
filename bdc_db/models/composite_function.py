from .base_sql import BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class CompositeFunction(BaseModel):
    __tablename__ = 'composite_functions'

    id = Column(String(20), primary_key=True, nullable=False, unique=True)
    collection_id = Column(ForeignKey('collections.id'), primary_key=True, nullable=False)
    description = Column(String(64))

    collection = relationship('Collection')