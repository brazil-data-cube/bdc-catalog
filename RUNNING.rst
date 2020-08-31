..
    This file is part of BDC-Catalog.
    Copyright (C) 2019-2020 INPE.

    BDC-Catalog is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Running BDC-Catalog in the Command Line
=======================================


Creating database definition
----------------------------

**1.** Create a PostgreSQL database and enable the PostGIS extension::

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db db init

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db db create-namespace

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db db create-extension-postgis


**2.** After that, run ``BDC-DB`` command to prepare the Brazil Data Cube data model::

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db alembic upgrade


**3.** The ``BDC-Catalog`` uses `PostgreSQL Triggers <https://www.postgresql.org/docs/12/plpgsql-trigger.html>`_ along database definition. Use the following command line to create default triggers::

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db db create-triggers


.. note::

        You can also check the available triggers with command::

                bdc-db db show-triggers

                Available triggers in "bdc_catalog.triggers"
                  -> /home/user/bdc-catalog/bdc_catalog/triggers/band_metadata_expression.sql
                  -> /home/user/bdc-catalog/bdc_catalog/triggers/collection_statistics.sql
                  -> /home/user/bdc-catalog/bdc_catalog/triggers/timeline.sql


Updating an Existing Data Model
-------------------------------

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db alembic upgrade


Updating the Migration Scripts
------------------------------

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db alembic revision "my revision" --branch=bdc_catalog


.. note::

        Make sure to pass ``--branch=bdc_catalog`` in order to prevent alembic branch tree.
