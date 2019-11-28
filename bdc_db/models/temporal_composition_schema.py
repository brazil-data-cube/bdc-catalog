from .base_sql import BaseModel
from sqlalchemy import Column, String


class TemporalCompositionSchema(BaseModel):
    __tablename__ = 'temporal_composition_schemas'

    id = Column(String(20), primary_key=True)
    temporal_composite_unit = Column(String(16), nullable=False)
    temporal_schema = Column(String(16), nullable=False)
    temporal_composite_t = Column(String(16), nullable=False)