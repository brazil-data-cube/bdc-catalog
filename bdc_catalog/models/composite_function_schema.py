#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sqlalchemy import Column, String, Integer, Text, UniqueConstraint

from .base_sql import BaseModel


class CompositeFunctionSchema(BaseModel):
    __tablename__ = 'composite_function_schemas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    description = Column(Text, nullable=False)
    alias = Column(String(6), nullable=False)

    __table_args__ = (
        UniqueConstraint(alias),
        UniqueConstraint(name),
    )
