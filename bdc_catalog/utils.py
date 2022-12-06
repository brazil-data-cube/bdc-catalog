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
"""Utility for Image Catalog Extension."""

import hashlib
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Tuple, Union

import geoalchemy2
import multihash as _multihash


def check_sum(file_path: Union[str, BytesIO], chunk_size=16384) -> bytes:
    """Read a file and generate a checksum using `sha256`.

    Raises:
        IOError when could not open given file.

    Args:
        file_path (str|BytesIo): Path to the file
        chunk_size (int): Size in bytes to read per iteration. Default is 16384 (16KB).

    Returns:
        The digest value in bytes.
    """
    algorithm = hashlib.sha256()

    def _read(stream):
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            algorithm.update(chunk)

    if isinstance(file_path, str) or isinstance(file_path, Path):
        with open(str(file_path), "rb") as f:
            _read(f)
    else:
        _read(file_path)

    return algorithm.digest()


def multihash_checksum_sha256(file_path: Union[str, BytesIO]):
    """Generate the checksum multihash.

    This method follows the spec `multihash <https://github.com/multiformats/multihash>`_.
    We use `sha256` as described in ``check_sum``. The multihash spec defines the code `0x12` for `sha256` and
    must have `0x20` (32 chars) length.

    See more in https://github.com/multiformats/py-multihash/blob/master/multihash/constants.py#L4

    Args:
        file_path (str|BytesIo): Path to the file

    Returns:
        A string-like hash in hex-decimal
    """
    sha256 = 0x12
    sha256_length = 0x20

    _hash = _multihash.encode(digest=check_sum(file_path), code=sha256, length=sha256_length)

    return _multihash.to_hex_string(_hash)


def geom_to_wkb(geom: Any, srid: int = None) -> geoalchemy2.WKBElement:
    """Create a WKB geometry from a shapely.geometry.Geometry.

    This helper uses the GeoAlchemy2 helper to ensure to create an extended WKB element (EWKB).
    It forces the SQLAlchemy field to load the Geometry into database with EWKB instead WKT
    to avoid any bit error precision.

    Note:
        Make sure you have installed extra ``geo`` or the library ``Shapely`` before::

            pip install Shapely

    Args:
        geom: A shapely Geometry
        srid: The Geometry SRID associated.
    """
    from geoalchemy2.shape import from_shape

    # Use extended=True to transform the geometry as EWKB
    return from_shape(geom, srid=-1 if srid is None else srid, extended=True)


def create_collection(name: str, version: Any, bands: list,
                      category: str = 'eo', **kwargs) -> Tuple['Collection', bool]:
    """Register a collection into database.

    Note:
        Used from :py:meth:`bdc_catalog.cli.load_data`
    """
    from bdc_catalog.models import (Band, Collection, GridRefSys, MimeType,
                                    ResolutionUnit, db)

    collection = (
        Collection.query()
        .filter(Collection.name == name,
                Collection.version == str(version))
        .first()
    )
    if collection is not None:
        return collection, False

    with db.session.begin_nested():
        collection = Collection(name=name, version=version)
        collection.collection_type = kwargs.get('collection_type', 'collection')
        collection.grs = GridRefSys.query().filter(GridRefSys.name == kwargs.get('grid_ref_sys')).first()
        collection.description = kwargs.get('description')
        collection.is_available = kwargs.get('is_available', True)
        collection.title = kwargs.get('title', collection.name)
        collection.category = category

        for band in bands:
            band_obj = Band(collection=collection, name=band['name'])
            for prop, value in band.items():
                if prop == 'mime_type':
                    band_obj.mime_type = MimeType.query().filter(MimeType.name == value).first()
                elif prop == 'resolution_unit':
                    band_obj.resolution_unit = ResolutionUnit.query().filter(ResolutionUnit.name == value).first()
                elif prop == 'metadata':  # Special case to avoid internal SQLAlchemy metadata prop
                    band_obj.metadata_ = value
                else:
                    setattr(band_obj, prop, value)
            db.session.add(band_obj)

        db.session.add(collection)
    db.session.commit()

    return collection, True


def create_item(collection_id: int, name: str,
                bbox: Any,
                footprint: Any,
                srid: int,
                start_date: Union[str, datetime],
                is_available: bool = True,
                **kwargs):
    """Command helper to register an item.

    Note:
        This helper does not check if item exists. Make sure to insert unique values
        otherwise may raise database unique constraint errors.

    Note:
        Used from :py:meth:`bdc_catalog.cli.load_data`

    Args:
        collection_id (int): The collection identifier
        name (str): The item name. It usually well-known as ``scene_id``.
        bbox (Any): The bbox shapely geometry.
            Make sure to pass EPSG:4326 geom.
        footprint (Any): The footprint shapely geometry.
            Make sure to pass EPSG:4326 geom.
        srid (int): Spatial reference system identifier.
            Make sure you have it in database.
        start_date (str|datetime): Item date.
        is_available (bool): Item availability. Defaults to ``True``.

    Keyword Args:
        end_date (Optional[str, datetime]): Item end date. Defaults to ``start_date``.
        cloud_cover (Optional[float]): Item cloud cover factor.
        provider_id (Optional[int]): The data provider identifier.
        tile_id (Optional[int]): Grid tile identifier
    """
    from bdc_catalog.models import Item, db

    with db.session.begin_nested():
        item = Item(name=name, collection_id=collection_id)
        item.bbox = geom_to_wkb(bbox, srid=4326)
        item.foot = geom_to_wkb(footprint, srid=4326)
        item.srid = srid
        item.is_available = is_available
        # Default end_date as start_date.
        item.start_date = item.end_date = start_date

        for key, value in kwargs.items():
            setattr(item, key, value)

        db.session.add(item)

    db.session.commit()

    return item
