from .base_sql import BaseModel
from sqlalchemy import Column, String


class GrsSchema(BaseModel):
    __tablename__ = 'grs_schemas'

    id = Column(String(20), primary_key=True)
    description = Column(String(64), nullable=False)
    crs = Column(String(400), nullable=True)