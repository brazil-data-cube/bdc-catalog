from .base_sql import BaseModel
from sqlalchemy import Column, Float, String


class RasterSizeSchema(BaseModel):
    __tablename__ = 'raster_size_schemas'

    id = Column(String(60), primary_key=True)
    raster_size_x = Column(Float(50), nullable=False)
    raster_size_y = Column(Float(50), nullable=False)
    raster_size_t = Column(Float(50))
    chunk_size_x = Column(Float(50), nullable=False)
    chunk_size_y = Column(Float(50), nullable=False)
    chunk_size_t = Column(Float(50))