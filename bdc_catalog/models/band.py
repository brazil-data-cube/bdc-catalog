#
# This file is part of BDC-Catalog.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Model for spectral bands and derived indices (table ``bdc.band``)."""

from typing import Optional, Tuple

from bdc_db.sqltypes import JSONB
from sqlalchemy import (Column, Enum, ForeignKey, Index, Integer, Numeric,
                        PrimaryKeyConstraint, String, Text)
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

    def add_eo_meta(self, resolution_x: float, resolution_y: float,
                    center_wavelength: Optional[float] = None, full_width_half_max: Optional[float] = None, **kwargs):
        """Set the EO properties to the band definition.

        .. versionadded:: 1.0.0

        This method follows the `STAC EO Extension for Bands <https://github.com/stac-extensions/eo#band-object>`_.

        Args:
            resolution_x: The sensor resolution in X.
            resolution_y: The sensor resolution in Y.
            center_wavelength: The center wavelength of the band, in micrometers (μm).
                The center wavelength is calculated from:
                ``center_wavelength = (min_wavelength + max_wavelength) / 2``.
            full_width_half_max: Full width at half maximum (FWHM).
                The width of the band, as measured at half the maximum transmission, in micrometers (μm).

        Keyword Args:
            solar_illumination (float): The solar illumination of the band, as measured at half the maximum transmission, in W/m2/micrometers.
        """
        props = self.properties
        props['resolution_x'] = resolution_x
        props['resolution_y'] = resolution_y
        if center_wavelength:
            props['center_wavelength'] = center_wavelength
        if full_width_half_max:
            props['full_width_half_max'] = full_width_half_max
        props.update(kwargs)
        if self.metadata_ is None:
            self.metadata_ = {}
        self.metadata_['eo'] = props
        # Copy a new object into instance to avoid internal prop matching using SA.
        self.metadata_ = self.metadata_.copy()


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
