..
    This file is part of BDC-Catalog.
    Copyright (C) 2019-2022 INPE.

    BDC-Catalog is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Running BDC-Catalog in the Command Line
=======================================

The Brazil Data Cube Catalog system uses the `Alembic Environment <https://alembic.sqlalchemy.org/en/latest/>`_
to upgrade/downgrade versions. If you would like to use it as experimental environments (dev only), you may consider to follow
`Development Mode`.

For production environment, we strongly recommend you to adopt alembic migration way to be able to support improvements.


Development Mode
----------------

**This step is not recommended for production environments. It will not generate alembic migration tree.**

For development purposes, we have prepared a command line `bdc-db db create-schema` to create all definitions for BDC-Catalog::

        export SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb"
        bdc-db db init
        bdc-db db create-namespaces
        bdc-db db create-extension-postgis
        lccs-db db create-extension-hstore
        bdc-db db create-schema


Creating database definition
----------------------------

**1.** Create a PostgreSQL database and enable the required extensions (`postgis`, `hstore`)::

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db db init

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db db create-namespaces

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db db create-extension-postgis

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        lccs-db db create-extension-hstore


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

        Make sure to pass ``--branch=bdc_catalog`` in order to generate the alembic migration into
        the same ``BDC-Catalog`` branch tree.
