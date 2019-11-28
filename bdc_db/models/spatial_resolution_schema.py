from .base_sql import BaseModel
from sqlalchemy import Column, Float, String


class SpatialResolutionSchema(BaseModel):
    __tablename__ = 'spatial_resolution_schemas'

    id = Column(String(20), primary_key=True)
    resolution_x = Column(Float(53), nullable=False)
    resolution_y = Column(Float(53), nullable=False)
    resolution_unit = Column(String(16), nullable=False)