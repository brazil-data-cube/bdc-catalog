from .base_sql import BaseModel
from geoalchemy2 import Geometry
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class Tile(BaseModel):
    __tablename__ = 'tiles'

    id = Column(String(20), primary_key=True, nullable=False, unique=True)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), primary_key=True, nullable=False)
    geom_wgs84 = Column(Geometry, index=True)
    geom = Column(Geometry)

    grs_schema = relationship('GrsSchema')