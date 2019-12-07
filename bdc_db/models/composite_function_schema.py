from .base_sql import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class CompositeFunctionSchema(BaseModel):
    __tablename__ = 'composite_function_schemas'

    id = Column(String(20), primary_key=True, nullable=False)
    description = Column(String(64))