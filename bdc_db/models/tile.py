from .base_sql import BaseModel
from geoalchemy2 import Geometry
from sqlalchemy import Column, ForeignKey, Index, String
from sqlalchemy.orm import relationship


class Tile(BaseModel):
    __tablename__ = 'tiles'
    __table_args__ = (
        Index('idx_tiles_geom_wgs84', 'geom_wgs84', postgres_using='gist'),
        Index('idx_tiles_geom', 'geom', postgres_using='gist'),
    )

    id = Column(String(20), primary_key=True, nullable=False)
    grs_schema_id = Column(ForeignKey('grs_schemas.id'), primary_key=True, nullable=False)
    geom_wgs84 = Column(Geometry(spatial_index=False))
    geom = Column(Geometry(spatial_index=False))

    grs_schema = relationship('GrsSchema')