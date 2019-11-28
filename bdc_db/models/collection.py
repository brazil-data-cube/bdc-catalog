from .base_sql import BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class Collection(BaseModel):
    __tablename__ = 'collections'

    id = Column(String(20), primary_key=True)
    spatial_resolution_schema_id = Column(ForeignKey('spatial_resolution_schemas.id'), nullable=False)
    temporal_composition_schema_id = Column(ForeignKey('temporal_composition_schemas.id'), nullable=False)
    raster_chunk_schema_id = Column(ForeignKey('raster_chunk_schemas.id'), nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), nullable=False)
    version = Column(String(16), nullable=False)
    description = Column(String(64), nullable=False)

    grs_schema = relationship('GrsSchema')
    raster_chunk_schema = relationship('RasterChunkSchema')
    spatial_resolution_schema = relationship('SpatialResolutionSchema')
    temporal_composition_schema = relationship('TemporalCompositionSchema')