from .base_sql import BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class Cube(BaseModel):
    __tablename__ = 'cubes'

    id = Column(String(20), primary_key=True)
    collection_id = Column(ForeignKey('collections.id'))
    composite_function_id = Column(ForeignKey('composite_functions.id'))
    oauth_info = Column(String(16))
    description = Column(String(64))

    composite_function = relationship('CompositeFunction')
    collection = relationship('Collection')