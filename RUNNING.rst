..
    This file is part of Brazil Data Cube Database module.
    Copyright (C) 2019 INPE.

    Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Running BDC-Catalog in the Command Line
=======================================


Creating database definition
----------------------------

**1.** Create a PostgreSQL database and enable the PostGIS extension:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db db init

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db db create-namespace

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db db create-extension-postgis


**2.** After that, run ``BDC-DB`` command to prepare the Brazil Data Cube data model:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:password@localhost:5432/bdcdb" \
        bdc-db alembic upgrade


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
