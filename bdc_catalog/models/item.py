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

"""Model for the image item of a collection."""

import mimetypes
import os
from datetime import datetime
from typing import List, Union

from geoalchemy2 import Geometry
from sqlalchemy import (TIMESTAMP, Boolean, Column, ForeignKey, Index, Integer,
                        Numeric, PrimaryKeyConstraint, String)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.sql import expression

from ..config import BDC_CATALOG_SCHEMA
from .base_sql import BaseModel, db
from .collection import Collection
from .processor import Processor
from ..utils import multihash_checksum_sha256

try:
    import rasterio
except ImportError:
    rasterio = None


class SpatialRefSys(db.Model):
    """Auxiliary model for the PostGIS spatial_ref_sys table."""

    __tablename__ = 'spatial_ref_sys'
    __table_args__ = ({"schema": "public", "extend_existing": True})

    srid = Column(Integer, primary_key=True)
    auth_name = Column(String)
    auth_srid = Column(Integer)
    srtext = Column(String)
    proj4text = Column(String)


class Item(BaseModel):
    """Model for the image item of a collection.

    An item is usually defined in Brazil Data Cube concept as a data product scene.

    The assets property follows the JSONSchema spec defined in :exc:`bdc_catalog.jsonschemas.item.assets.json`,
    which uses the function :meth:`bdc_catalog.utils.multihash_checksum_sha256` to generate the file checksum.

    The following example describes an published item of a Sentinel-2 data product scene ``S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053``::

        {
            "id": 423658,
            "name": "S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053",
            "collection_id": 23, # Collection S2_L1C
            "start_date": "2019-10-18T13:42:11",
            "end_date": "2019-10-18T13:42:11",
            "footprint": POLYGON((-50.094208 -7.23638395134798,-49.099884 -7.23332135700407,-49.09546 -8.22598479222442,-50.09207 -8.22947294680053,-50.094208 -7.23638395134798))",
            "bbox": "POLYGON((-49.09545 -8.225985,-49.099896 -7.233321,-50.094195 -7.236384,-50.092074 -8.229473,-49.09545 -8.225985))",
            "srid": 4326,
            "assets": {
                "thumbnail": {
                    "href": "/Repository/Archive/S2_L1C/v001/22/M/FS/2019/S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053/S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053.png",
                    "type": "image/png",
                    "roles": [
                        "thumbnail"
                    ],
                    "created": "2020-12-16T18:50:05",
                    "updated": "2020-12-16T18:50:05",
                    "bdc:size": 183439,
                    "checksum:multihash": "1220476cf4b62525f99e9891634acdd3c4fbfc151e407e762ee8b32ce7ba72824a41"
                },
                "asset": {
                    "href": "/Repository/Archive/S2_L1C/v001/22/M/FS/2019/S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053/S2A_MSIL1C_20191018T134211_N0208_R124_T22MFS_20191018T152053.zip",
                    "type": "application/zip",
                    "roles": [
                        "data"
                    ],
                    "created": "2020-12-16T18:50:05",
                    "updated": "2020-12-16T18:50:05",
                    "bdc:size": 789501813,
                    "checksum:multihash": "1220f1cebeff261104a35b7ce68083777cf3449a733acf240120ccf949d5c758e31a"
                }
            }
        }
    """

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    is_available = Column(Boolean, default=False, nullable=False, server_default=expression.false())
    collection_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.collections.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    tile_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.tiles.id', onupdate='CASCADE', ondelete='CASCADE'))
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    cloud_cover = Column(Numeric)
    assets = Column(JSONB('bdc-catalog/item-assets.json'), comment='Follow the JSONSchema @jsonschemas/item-assets.json')
    metadata_ = Column('metadata', JSONB('bdc-catalog/item-metadata.json'),
                       comment='Follow the JSONSchema @jsonschemas/item-metadata.json')
    provider_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.providers.id', onupdate='CASCADE', ondelete='CASCADE'))
    bbox = Column(Geometry(geometry_type='Polygon', srid=4326, spatial_index=False))
    footprint = Column(Geometry(geometry_type='Polygon', srid=4326, spatial_index=False))
    srid = Column(Integer, ForeignKey('public.spatial_ref_sys.srid', onupdate='CASCADE', ondelete='CASCADE'))

    collection = relationship(Collection)
    tile = relationship('Tile')

    __table_args__ = (
        Index(None, cloud_cover),
        Index(None, collection_id),
        Index(None, bbox, postgresql_using='gist'),
        Index(None, footprint, postgresql_using='gist'),
        Index(None, name),
        Index(None, is_available),
        Index(None, provider_id),
        Index('idx_items_start_date_end_date', start_date, end_date),
        Index(None, tile_id),
        Index(None, start_date),
        Index('idx_bdc_items_start_date_desc', start_date.desc()),
        Index(None, metadata_),
        dict(schema=BDC_CATALOG_SCHEMA),
    )

    @property
    def processors(self) -> List['Processor']:
        """The processors used that the item were generated."""
        return ItemsProcessors.get_processors(self.id)

    def save(self, commit=True):
        """Overwrite the BaseModel.save and update the assets metadata.

        Note:
            This method uses
            `SQLAlchemy flag_modified <https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.attributes.flag_modified>`_
            to detect any change in ``assets``.
        """
        now = datetime.utcnow()
        now_str = now.strftime('%Y-%m-%dT%H:%M:%S')

        self.updated = now

        if self.assets:
            for asset in self.assets.values():
                asset['updated'] = now_str

            # Trick to SQLAlchemy be aware that the field was changed.
            flag_modified(self, "assets")

        super().save(commit=commit)

    def add_asset(self, name: str, file: str, role: List[str], href: str, **kwargs):
        """Add a new asset in Item context.

        .. versionadded:: 1.0.0

        Note:
            If asset name already exists, it overwrites the asset definition.

        Raises:
            ValueError: When could not determine mimetype relationship.

        Examples:
            This example represent a minimal way to generate ``Item.assets`` that
            follows `STAC Item Spec <https://stacspec.org/en/about/stac-spec/>`_.

            .. doctest::
                :skipIf: True

                >>> item = Item(name='LC8-16D_V1_007011_20200101', collection_id=4)
                >>> item.cloud_cover = 30.2
                >>> item.start_date = '2020-01-01'
                >>> item.end_date = '2020-01-16'
                >>> item.add_asset('EVI', '/path/to/EVI.tif', role=['data'],
                ...                href='/cubes/LC8/007011/2020/01/01/EVI.tif')
                >>> item.add_asset('thumbnail', '/path/to/thumbnail.png', role=['thumbnail'],
                ...                href='/cubes/LC8/007011/2020/01/01/thumbnail.png')
                >>> item.save()

        Args:
            name (str): Asset name
            file (str): Absolute file path
            role (List[str]) - Asset role. Available values are: ['data'], ['thumbnail']
            href (str): Relative file path for item asset.

        Keyword Args:
            **kwargs: All optional attributes specified in :meth:`bdc_catalog.models.Item.create_asset_definition`.
            mime_type (str): Custom mime type for item asset.
                When no mime type is set, it tries to find in :attr:`bdc_catalog.models.Band.mime_type`.
                When there is no band relation and the value is ``None``, it will raise ``ValueError``.
                Defaults to ``None``.
        """
        self.assets = self.assets or {}
        mime_type = kwargs.get('mime_type')
        if mime_type is None:
            # Seek in band
            if self.collection_id is None:
                raise ValueError('Could not determine Mimetype when Item collection is None.')
            collection = self.collection
            mime_type = mimetypes.guess_type(os.path.basename(file))[0]
            if collection is None:
                collection = Collection.get_by_id(self.collection_id)
            for band in collection.bands:
                if band.name == name:
                    mime_type = band.mime_type.name if band.mime_type else None
                    break
            if mime_type is None:
                raise ValueError(f'Could not determine Mimetype for Asset "{name}" when Band.mime_type is None.')

            kwargs['mime_type'] = mime_type

        self.assets[name] = self.create_asset_definition(file=file, role=role, href=href, **kwargs)

    @classmethod
    def create_asset_definition(cls, file: str, role: List[str], href: str, mime_type: str,
                                checksum: bool = True,
                                created_at: Union[datetime, str] = None,
                                fmt: str = '%Y-%m-%dT%H:%M:%S',
                                is_raster: bool = False,
                                **kwargs):
        """Create Item Asset structure.

        .. versionadded:: 1.0.0

        This method follows the `STAC Item Spec <https://stacspec.org/en/about/stac-spec/>`_.

        Note:
            If the parameter ``is_raster`` is set, make sure you have ``rasterio`` installed.

        Args:
            file (str): The absolute file path
            role (List[str]) - Asset role. Available values are: ['data'], ['thumbnail']
            href (str): Relative file path for item asset.
            mime_type (str): Custom mime type for item asset.
            checksum (bool) - Flag to generate checksum. Defaults to ``True``.
                The algorithm used is sha256.
            created_at (datetime|str): The value indicating when asset were created.
                Defaults to ``None``, which means to ``utc now``.
            fmt (str): The datetime format for ``created`` and ``updated`` fields.
            is_raster (bool): Flag to generate Raster metadata in Asset. Defaults to ``False``.

        Keyword Args:
            **kwargs: Any extra field value for Asset definition.
                You may use this keyword arg to specify for own spec attribute.
        """
        _now_str = datetime.utcnow().strftime(fmt)
        created = _now_str

        if isinstance(created_at, datetime):
            created = created_at.strftime(fmt)

        asset = {
            'href': str(href),
            'type': mime_type,
            'bdc:size': os.stat(file).st_size,
            'roles': role,
            'created': created,
            'updated': _now_str
        }
        asset.update(**kwargs)
        if checksum:
            asset['checksum:multihash'] = multihash_checksum_sha256(str(file))

        if is_raster:
            if rasterio is None:
                raise ImportError('Missing library "rasterio" to generate Item.assets')

            with rasterio.open(str(file)) as data_set:
                asset['bdc:raster_size'] = dict(
                    x=data_set.shape[1],
                    y=data_set.shape[0],
                )

                chunk_x, chunk_y = data_set.profile.get('blockxsize'), data_set.profile.get('blockxsize')

                if chunk_x is None or chunk_x is None:
                    return asset

                asset['bdc:chunk_size'] = dict(x=chunk_x, y=chunk_y)

        return asset

    def add_processor(self, processor: Processor) -> 'ItemsProcessors':
        """Attach a processor into item scope.

        Note:
            May raise error when processor is already attached.

        Args:
            processor (Processor): Instance of Processor
        """
        item_processor = ItemsProcessors()
        item_processor.item = self
        item_processor.processor = processor
        db.session.add(item_processor)
        return item_processor


class ItemsProcessors(BaseModel):
    """Represent model to integrate with STAC Extension Processing.

    See More in `Processing Extension Specification <https://github.com/stac-extensions/processing>`_.
    """

    __tablename__ = 'items_processors'

    item_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.items.id', onupdate='CASCADE', ondelete='CASCADE'),
                     nullable=False)
    processor_id = Column(ForeignKey(f'{BDC_CATALOG_SCHEMA}.processors.id', onupdate='CASCADE', ondelete='CASCADE'),
                          nullable=False)

    item = relationship(Item)
    processor = relationship(Processor)

    __table_args__ = (
        PrimaryKeyConstraint(item_id, processor_id),
        dict(schema=BDC_CATALOG_SCHEMA),
    )

    @classmethod
    def get_processors(cls, item_id: int) -> List[Processor]:
        """Retrieve the processors related to Item."""
        entries = (
            db.session.query(Processor)
            .join(ItemsProcessors, ItemsProcessors.processor_id == Processor.id)
            .filter(ItemsProcessors.item_id == item_id)
            .all()
        )
        return entries
