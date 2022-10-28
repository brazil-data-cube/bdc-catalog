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

This tutorial covers the well known usage of ``BDC-Catalog`` data management integrating with Python
`SQLAlchemy <https://www.sqlalchemy.org/>`_.
Its applicable to users who want to learn how to use ``Brazil Data Cube Catalog`` module in runtime and
for users that have existing applications or related learning material for ``BDC-Catalog``.


Requirement
-----------

For this tutorial, we will use an instance of PostgreSQL with PostGIS support
``SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost/bdcdb``
You can set up a minimal PostgreSQL instance with Docker with the following command:

.. code-block:: shell

    docker run --name bdc_pg \
               --detach \
               --volume bdc_catalog_vol:/var/lib/postgresql/data \
               --env POSTGRES_PASSWORD=postgres \
               --publish 5432:5432 \
               postgis/postgis:12-3.0


.. note::

    You may, optionally, skip this step if you have already a running PostgreSQL with PostGIS supported.

.. note::

    Consider to have a minimal module init as mentioned in :doc:`Usage - Development <usage>`.
    You may use the following statement to initialize through Python context:

    .. code-block:: python
        :emphasize-lines: 8-10

        from bdc_catalog import BDCCatalog
        from flask import Flask

        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bdc'
        BDCCatalog(app)

        with app.app_context():
            # Any operation related database here
            pass


    Since the ``BDC-Catalog`` were designed to work with Flask API framework, remember to always use it while ``app.app_context()`` as above.



BDC-Catalog & STAC Spec
-----------------------

The ``BDC-Catalog`` was proposed to implement the `STAC Spec <https://stacspec.org/en/about/stac-spec/>`_.
The STAC Spec is a way to standardize the geospatial assets metadata as catalog along the service applications.
With the database model ``BDC-Catalog``, the Brazil Data Cube implements the STAC API Spec in the module
`BDC-STAC <https://bdc-stac.readthedocs.io/en/latest/>`_. Currently, the ``BDC-STAC`` is supporting the STAC API 1.0.

The diagram depicted in the figure below contains the most important concepts behind the STAC data model:

.. image:: https://brazil-data-cube.github.io/_images/stac-model.png
   :target: https://brazil-data-cube.github.io/_images/stac-model.png

The description of the concepts below are adapted from the STAC Specification:

- ``Item``: a STAC Item is the atomic unit of metadata in STAC, providing links to the actual assets (including thumbnails) that they represent. It is a GeoJSON Feature with additional fields for things like time, links to related entities and mainly to the assets. According to the specification, this is the atomic unit that describes the data to be discovered in a STAC Catalog or Collection.

- ``Asset``: a spatiotemporal asset is any file that represents information about the earth captured in a certain space and time.

- ``Catalog``: provides a structure to link various STAC Items together or even to other STAC Catalogs or Collections.

- ``Collection``: is a specialization of the Catalog that allows additional information about a spatiotemporal collection of data.

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

.. literalinclude:: ../../examples/create_collection.py
   :language: python
   :lines: 21-


You can also create a collection using a minimal func helper named :func:`bdc_catalog.utils.create_collection`:

.. code-block:: python

    from bdc_catalog.utils import create_collection

    create_collection(name='S2_L1C', version='1', title='Sentinel-2 - MSI - Level-1C', **parameters)


.. note::

    Optionally, you can load a ``Collection`` using a minimal command line from :func:`bdc_catalog.cli.load_data`:

    .. code-block:: shell

        bdc-catalog load-data --ifile examples/fixtures/sentinel-2.json


Create Band
+++++++++++

The model :class:`bdc_catalog.models.Band` aggregates the collection,
Optionally, you may set extra metadata for a band using :class:`bdc_catalog.models.MimeType` and :class:`bdc_catalog.models.ResolutionUnit`.

The model :class:`bdc_catalog.models.MimeType` deals with supported content types for :class:`bdc_catalog.models.Band`
and indicates the nature and format of ``assets``.

.. literalinclude:: ../../examples/create_mimetypes.py
   :language: python
   :lines: 24-


The model :class:`bdc_catalog.models.ResolutionUnit` specifies the unit spatial resolution for :class:`bdc_catalog.models.Band`.
So it can be represented as: `Meter (m)`, `degree`, `centimeters (cm)`, etc. The following snippet is used to create a new
resolution unit.

.. code-block:: python
    :name: create-resolution-py

    from bdc_catalog.models import ResolutionUnit

    resolutions = [
        ('Meter', 'm'),
        ('Centimeter', 'cm'),
        ('Degree', '°')
    ]

    for name, symbol in resolutions:
        res = ResolutionUnit()
        res.name = name
        res.symbol = symbol
        res.save()


Access Collections
++++++++++++++++++

In order to search for Collections, please, take a look in the next query. To retrieve all collections from database use:

.. literalinclude:: ../../examples/query_collections.py
   :language: python
   :lines: 24-40

You can increment the query and restrict to show only ``available`` collections:


.. literalinclude:: ../../examples/query_collections.py
   :language: python
   :lines: 24-34,42-48


A collection, essentially, has a few unique keys. Its defined by both ``id`` and ``Name-Version``.

.. literalinclude:: ../../examples/query_collections.py
   :language: python
   :lines: 24-34,50-59


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

.. note::

    This is just an example of how to publish an item in ``BDC-Catalog``. You must need to have the directory containing the mentioned files to execute the example properly.


Consider you have a directory named ``S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627``
containing a set of files to publish:

- ``S2A_MSIL1C_20210527T150721_N0300_R082_T19LBL_20210527T183627``:

  - ``B02.tif``
  - ``B03.tif``
  - ``B04.tif``
  - ``thumbnail.png``

You can register this item as following:

.. literalinclude:: ../../examples/create_item.py
   :language: python
   :lines: 26-


Access Items
++++++++++++

In order to search for Items, please, take a look in the simple query.
Consider you have a ``collection`` instance object. To retrieve all items from the given collection,
use as following:

.. literalinclude:: ../../examples/query_items.py
   :language: python
   :lines: 25-42
   :emphasize-lines: 17


You can also increment the query, delimiting restriction of ``cloud_cover`` less than ``50%`` (only available items):


.. literalinclude:: ../../examples/query_items.py
   :language: python
   :lines: 25-37,46-54
   :emphasize-lines: 17,18


Since the ``BDC-Catalog`` integrates with ``SQLAlchemy ORM``, you can join relationship tables and then query by :class:`bdc_catalog.models.Tile` for example:


.. literalinclude:: ../../examples/query_items.py
   :language: python
   :lines: 25-37,56-64
   :emphasize-lines: 16,18


.. note::

    Whenever the entry ``Item.query()`` is used, it retrieves `ALL` columns from :class:`bdc_catalog.models.Item`.
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

.. literalinclude:: ../../examples/item_processors.py
   :language: python
   :lines: 21-40


To attach the item with
`Sen2Cor <https://step.esa.int/main/snap-supported-plugins/sen2cor/>`_, you may use as following:

.. literalinclude:: ../../examples/item_processors.py
   :language: python
   :lines: 21-30,42-


.. note::

    Optionally, you may use the verbose way manually relating :class:`bdc_catalog.models.Item` and :class:`bdc_catalog.models.Processor` using :class:`bdc_catalog.models.ItemsProcessors` as following:

    .. code-block:: python

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
