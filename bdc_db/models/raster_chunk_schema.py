from .base_sql import BaseModel
from sqlalchemy import Column, Integer, String


class RasterChunkSchema(BaseModel):
    __tablename__ = 'raster_chunk_schemas'

    id = Column(String(20), primary_key=True)
    raster_size_x = Column(Integer)
    raster_size_y = Column(Integer)
    raster_size_t = Column(Integer)