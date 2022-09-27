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

The ``BDC-Catalog`` was proposed to implement the ``STAC-Spec``.
TODO: Describe relationship between ``BDC-Catalog`` and `STAC Spec <https://stacspec.org/en/about/stac-spec/>`_


.. image:: https://brazil-data-cube.github.io/_images/stac-model.png
   :target: https://brazil-data-cube.github.io/_images/stac-model.png

.. collection_:

Collection Management
---------------------

The model :class:`bdc_catalog.models.Collection` follows the signature of `STAC Collection Spec <https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md>`_.
A ``collection`` is a specialization of the Catalog that allows additional information about a spatiotemporal collection of data.
In :class:`bdc_catalog.models.Collection`, we have the ``fields`` as described below:

- ``title``: A short descriptive title for the Collection.
- ``name``: A short name representation for the Collection. This value act as Unique value when combined with ``version`` with following signature: ``name-version``.
- ``description``: A detailed description to fully explain the collection.
- ``version``: Version definition. This value act as Unique value when combined with ``name`` with following signature: ``name-version``.
- ``properties``: A map of collection properties like sensor, platform, etc. This field is combined and shown in STAC Server.
- ``is_available``: Flag to determine the Collection availability. When value is ``False`` means that collection should not be shown in ``Catalog``.
- ``keywords``: List of keywords describing the collection. This field is used in STAC Server.
- ``collection_type``: Enum type to describe the collection. The supported values are: ``collection``, ``cube``, ``classification`` and ``mosaic``.
- ``category``: Enum type to identify collection kind. The supported values are:

  - ``eo`` for Electro-Optical sensors
  - ``sar`` for Synthetic-Aperture Radar sensors,
  - ``lidar`` for LiDAR imagery
  - ``unknown`` for others datasets.
- ``temporal_composition_schema``: A structure representing the temporal step which the collection were built. This field is `OPTIONAL`.
  Follows the `BDC Temporal Compositing <https://brazil-data-cube.github.io/products/specifications/processing-flow.html#temporal-compositing>`_.
- ``composite_function_id``: The Temporal Compositing function used to generate a data cube. This field is `OPTIONAL`.


Create Collection
+++++++++++++++++

As mentioned in the section `Collection Management <collection>`_, the model :class:`bdc_catalog.models.Collection` requires a few fields to be
filled out. A minimal way to create collection is:

.. code-block:: python

    from bdc_catalog.models import Collection

    collection = Collection()
    collection.name = 'S2_L1C'
    collection.version = '1'
    collection.title = 'Sentinel-2 - MSI - Level-1C'
    collection.properties = {
        "platform": "sentinel-2",
        "instruments": [
            "MSI"
        ]
    }
    collection.category = 'eo'
    collection.collection_type = 'collection'
    collection.keywords = ["eo", "sentinel", "msi"]
    collection.is_available = True
    collection.save()


We have prepared a minimal func helper to pre-set named :func:`bdc_catalog.utils.create_collection`:

.. code-block:: python

    from bdc_catalog.utils import create_collection

    create_collection(name='S2_L1C', version='1', title='Sentinel-2 - MSI - Level-1C', **parameters)


.. note::

    Optionally, you can load a ``Collection`` using a minimal command line from :func:`bdc_catalog.cli.load_data`:

    .. code-block:: shell

        bdc-catalog load-data --ifile examples/fixtures/sentinel-2.json


Create Band
+++++++++++

TODO:


Access Collections
++++++++++++++++++

In order to search for Items, please, take a look in the next query. To retrieve all collections from database use:

.. code-block:: python

    collections = (
        Collection.query()
        .all()
    )

You can increment the query and restrict to show only ``available`` collections:


.. code-block:: python
    :emphasize-lines: 3

    collections = (
        Collection.query()
        .filter(Collection.is_available.is_(True))
        .all()
    )


A collection, essentially, has a few unique keys. Its defined by both ``id`` and ``Name-Version``.

.. code-block:: python
    :name: create-collection-py

    from bdc_catalog.models import Collection

    collection = Collection.get_by_id("S2_L1C-1")  # or Collection.get_by_id(TheIntUniqueId)
    collection

    # Or verbose way
    collection = (
        Collection.query()
        .filter(Collection.identifier == "S2_L1C-1")  # or Collection.id == TheIntUniqueId
        .first()
    )


.. item_:

Item Management
---------------

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
- ``bbox``: Item footprint bounding box. It consists in a ``Geometry(Polygon, 4326)``.


Create Item
+++++++++++

Consider you have a directory named ``S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627``
containing a set of files to publish:

- ``S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627``:

  - ``B02.tif``
  - ``B03.tif``
  - ``B04.tif``
  - ``thumbnail.png``

You can register this item as following:

.. code-block:: python
    :name: create-item-py

    import shapely.geometry
    # We recommend to import bdc_catalog.utils.geom_to_wkb to transform shapely GEOM to WKB
    from bdc_catalog.utils import geom_to_wkb

    name = "S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627"
    geometry = shapely.geometry.shape({
        "type": "Polygon",
        "coordinates": [[[-70.731002, -9.131078],
                         [-70.726482, -8.138363],
                         [-71.722423, -8.132908],
                         [-71.729545, -9.124947],
                         [-70.731002, -9.131078]]]
    })

    # Lets create a new Item definition
    item = Item(collection_id=collection.id, name=name)
    item.cloud_cover = 0
    item.start_date = item.end_date = "2021-05-27T15:07:21"
    item.footprint = geom_to_wkb(geometry, srid=4326)
    item.bbox = geom_to_wkb(geometry.bbox, srid=4326)
    item.is_available = True
    for band in ['B02.tif', 'B03.tif', 'B04.tif', 'thumbnail.png']:
        item.add_asset(name=band,
                       file=f"S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627/{band}",
                       role=["data"],
                       href=f"/s2-l1c/19/L/BL/2021/S2A_MSIL1C_20210527T150721_1/{band}")
    item.save()


Access Items
++++++++++++

In order to search for Items, please, take a look in the simple query.
Consider you have a ``collection`` instance object. To retrieve all items from the given collection,
use as following:

.. code-block:: python
    :emphasize-lines: 3

    items = (
        Item.query()
        .filter(Item.collection_id == collection.id)
        .all()
    )

You can also increment the query, delimiting restriction of ``cloud_cover`` less than ``50%`` (only available items):


.. code-block:: python
    :emphasize-lines: 4-5

    items = (
        Item.query()
        .filter(Item.collection_id == collection.id,
                Item.cloud_cover <= 50,
                Item.is_available.is_(True))
        .order_by(Item.start_date.desc())
        .all()
    )


.. note::

    Whenever the entry ``Item.query()`` is used, it retrieves ALL columns from :class:`bdc_catalog.models.Item`.
    Depending your application, you may face performance issues due total amount of affected items.
    Since we are integrating with SQLAlchemy, you can specify desirable fields as following:

    .. code-block:: python
        :emphasize-lines: 4

        from bdc_catalog.models import db

        items = (
            db.session.query(Item.name, Item.cloud_cover, Item.assets)
            .filter(Item.collection_id == collection.id,
                    Item.cloud_cover <= 50,
                    Item.is_available.is_(True))
            .order_by(Item.start_date.desc())
            .all()
        )
        for item in items:
            # It injects `.name`, `.cloud_cover`, `.assets` by default in SQLAlchemy
            print(item.name)

    Essentially, the query structure is similar. Keep in mind that the given query retrieves only
    specified fields. With this, you don't have a reference to the :class:`bdc_catalog.models.Item`.


Processor & ItemsProcessors
---------------------------

The model :class:`bdc_catalog.models.ItemsProcessors` extends the :class:`bdc_catalog.models.Item` adding support to
relate Items with :class:`bdc_catalog.models.Processor`, similar in `STAC Processing <https://github.com/stac-extensions/processing>`_.
In other words, it indicates from which processing chain the :class:`bdc_catalog.models.Item` originates and
how the data itself has been produced. It makes a Item traceability and search among the processing levels.
A processor can be created as following:

.. code-block:: python
    :name: create-processor-py

    from bdc_catalog.models import Processor, db

    with db.session.begin_nested():
        processor = Processor()
        processor.name = 'Sen2Cor'
        processor.facility = 'Copernicus Sentinel-2 Level 2A'
        processor.level = 'L2A'
        processor.version = '2.10'
        processor.uri = 'https://step.esa.int/main/snap-supported-plugins/sen2cor/'
        processor.save(commit=False)
    db.session.commit()


To attach the item with
`Sen2Cor <https://step.esa.int/main/snap-supported-plugins/sen2cor/>`_, you may use as following:

.. code-block:: python
    :name: item-processor-py

    from bdc_catalog.models import ItemsProcessors, db

    with db.session.begin_nested():
        item_processor = ItemsProcessors()
        item_processor.item_id = item.id
        item_processor.processor = processor
        item_processor.save(commit=False)

    db.session.commit()

After make a relationship between ``Item`` and ``Processor`` using ``ItemsProcessors``, you can access the
relationship with command:

.. code-block:: python

    item.get_processors()


Mime Types
----------

The model :class:`bdc_catalog.models.MimeType` deals with supported content types for :class:`bdc_catalog.models.Band`
and indicates the nature and format of ``assets``.

.. code-block:: python
    :name: create-mime-py
    :caption: Example how to create mime types

    from bdc_catalog.models import MimeType

    mimetypes = [
        'image/png',
        'image/tiff', 'image/tiff; application=geotiff',
        'image/tiff; application=geotiff; profile=cloud-optimized',
        'text/plain',
        'text/html',
        'application/json',
        'application/geo+json',
        'application/x-tar',
        'application/gzip'
    ]

    for mimetype in mimetypes:
        mime = MimeType(name=mimetype)
        mime.save()
