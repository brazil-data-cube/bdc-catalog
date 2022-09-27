..
    This file is part of BDC-Catalog.
    Copyright (C) 2022 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.


Tutorial
========

BDC-Catalog & STAC Spec
-----------------------

TODO: Describe relationship between ``BDC-Catalog`` and `STAC Spec <https://stacspec.org/en/about/stac-spec/>`_


.. image:: https://brazil-data-cube.github.io/_images/stac-model.png
   :target: https://brazil-data-cube.github.io/_images/stac-model.png


Collection
----------

TODO:

We have prepared a minimal way to register Collection::

    bdc-catalog load-data --ifile examples/fixtures/sentinel-2.json


.. code-block:: python

    from bdc_catalog.models import Collection

    collection = Collection.get_by_id("S2_L1C-1")
    collection


Item
----

The model :class:`bdc_catalog.models.Item` follows the assignature of STAC Spec definition.
According to `STAC Spec Item <https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md>`_, an item
represents an atomic collection of inseparable data and metadata, which its geo-located feature using `GeoJSON Spec <https://geojson.org/>`_ with additional
fields for things like time, links to related entities and mainly to the assets.
The STAC Item has ``Assets`` which file that represents information about the earth captured in a certain space and time.
In :class:`bdc_catalog.models.Item`, we have the ``fields`` as described below:

- ``cloud_cover``: Field describing the cloud cover factor. It will be transpiled as ``eo:cloud_cover`` in ``STAC Item properties``.
- ``is_available``: Flag to determine the Item availability. When value is ``False`` means that item should not be shown in ``Catalog``.
- ``tile_id``: Tile identifier relationship of Item.
- ``metadata``: The metadata related with Item. All properties inside this field acts like ``STAC Item properties``.
- ``provider_id``: Item origin. Follows the `STAC Provider Object <https://github.com/radiantearth/stac-spec/blob/v1.0.0/collection-spec/collection-spec.md#provider-object>`_.
- ``footprint``: Item footprint geometry. It consists in a ``Geometry(Polygon, 4326)``. As others modern GIS applications, we recommend that ``footprint`` should be
  simplified geometry.
- ``bbox``: Item footprint bouding box. It consists in a ``Geometry(Polygon, 4326)``.


Create Item
+++++++++++

Let's support we have a following directory ``S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627`` containing a set of bands to
publish:

- ``S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627``:

  - ``B02.tif``
  - ``B03.tif``
  - ``B04.tif``
  - ``thumbnail.png``

We have prepared a minimal way to register Item::

    import shapely.geometry
    # We recommend to import bdc_catalog.utils.geom_to_wkb
    # to transform shapely GEOM to WKB
    from bdc_catalog.utils import geom_to_wkb

    name = "S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627"
    geometry = shapely.geometry.shape(
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [-70.731002, -9.131078],
                    [-70.726482, -8.138363],
                    [-71.722423, -8.132908],
                    [-71.729545, -9.124947],
                    [-70.731002, -9.131078]
                ]
            ]
        })

    # Lets create a new Item definition
    item = Item(collection_id=collection.id, name=name)
    item.cloud_cover = 0
    item.start_date = item.end_date = "2021-05-27T15:07:21"
    item.footprint = geom_to_wkb(geometry, srid=4326)
    item.bbox = geom_to_wkb(geometry.bbox, srid=4326)
    for band in ['B02.tif', 'B03.tif', 'B04.tif', 'thumbnail.png']:
        item.add_asset(name=band,
                       file=f"S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627/{band}",
                       role=["data"],
                       href=f"/s2-l1c/19/L/BL/2021/S2A_MSIL1C_20210527T150721_1/{band}")
    item.save()
