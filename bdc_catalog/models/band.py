#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Model for spectral bands and derived indices (table ``bdc.band``)."""

from typing import Optional, Tuple

from bdc_db.sqltypes import JSONB
from sqlalchemy import (Column, Enum, ForeignKey, Index, Integer, Numeric,
                        PrimaryKeyConstraint, String, Text)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel
from .collection import Collection

name_data_type = 'data_type'
options_data_type = ('uint8', 'int8', 'uint16', 'int16', 'uint32', 'int32', 'float32', 'float64')
enum_data_type = Enum(*options_data_type, name=name_data_type)


class Band(BaseModel):
    """Model for spectral bands and derived indices (table ``bdc.band``).

    A band consists in description of the matrix band values and data storage.
    """

    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    common_name = Column(String(255), nullable=False)
    description = Column(Text)
    min_value = Column(Numeric)
    max_value = Column(Numeric)
    nodata = Column(Numeric)
    scale_mult = Column(Numeric, comment='The scale value multiplier')
    scale_add = Column(Numeric, comment='The value to sum in scale mult')
    collection_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.collections.id', onupdate='CASCADE', ondelete='CASCADE'))
    resolution_unit_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.resolution_unit.id', onupdate='CASCADE', ondelete='CASCADE'))
    data_type = Column(enum_data_type)
    mime_type_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.mime_type.id', onupdate='CASCADE', ondelete='CASCADE'))
    metadata_ = Column('metadata', JSONB('bdc-catalog/band-metadata.json'),
                       comment='Follow the JSONSchema @jsonschemas/band-metadata.json')

    collection = relationship(Collection, back_populates='bands')
    resolution_unit = relationship('ResolutionUnit')
    mime_type = relationship('MimeType', back_populates='bands')

    __table_args__ = (
        Index(None, collection_id),
        Index(None, name),
        Index(None, common_name),
        Index(None, mime_type_id),
        Index(None, resolution_unit_id),
        dict(schema=BDC_CATALOG_SCHEMA),
    )

    @property
    def properties(self):
        """Retrieve the metadata related STAC Properties for a band."""
        if self.collection is None or self.metadata_ is None:
            return {}
        category = self.collection.category
        return self.metadata_.get(category) or {}

    @property
    def eo_resolutions(self) -> Optional[Tuple[float, float]]:
        """Retrieve the EO Band resolution X, Y."""
        props = self.properties
        resx, resy = props.get('resolution_x'), props.get('resolution_y')
        if resx is None or resy is None:
            return None
        return resx, resy

class BandSRC(BaseModel):
    """Model for band provenance/lineage."""

    __tablename__ = 'band_src'

    band_id = Column(
        'band_id', Integer(),
        ForeignKey(Band.id, onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )

    band_src_id = Column(
        'band_src_id',
        Integer(),
        ForeignKey(Band.id, onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint(band_id, band_src_id),
        dict(schema=BDC_CATALOG_SCHEMA),
    )
