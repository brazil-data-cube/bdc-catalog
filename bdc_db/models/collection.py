from .base_sql import BaseModel
from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship


class Collection(BaseModel):
    __tablename__ = 'collections'

    id = Column(String(20), primary_key=True)
    temporal_composition_schema_id = Column(ForeignKey('temporal_composition_schemas.id'), nullable=True)
    raster_size_schema_id = Column(ForeignKey('raster_size_schemas.id'), nullable=True)
    composite_function_schema_id = Column(ForeignKey('composite_function_schemas.id'), nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), nullable=False)
    sensor = Column(String(40), nullable=True)
    geometry_processing = Column(String(16), nullable=True)
    radiometric_processing = Column(String(40), nullable=True)
    description = Column(String(250), nullable=False)
    oauth_scope = Column(String(250), nullable=True)
    is_cube = Column(Boolean, nullable=True, default=False)
    bands_quicklook = Column(String(250), nullable=True)

    grs_schema = relationship('GrsSchema')
    composite_function_schemas = relationship('CompositeFunctionSchemas')
    raster_size_schemas = relationship('RasterSizeSchemas')
    temporal_composition_schema = relationship('TemporalCompositionSchema')