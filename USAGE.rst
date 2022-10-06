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


Usage
=====

The Brazil Data Cube Catalog system uses the `Alembic Environment <https://alembic.sqlalchemy.org/en/latest/>`_
to upgrade/downgrade versions. If you would like to use it as experimental environments (dev only), you may consider to follow
`Development Mode`.

For production environment, we strongly recommend you to adopt alembic migration way to be able to support improvements.


Development Mode
----------------

.. note::

    This step is not recommended for production environments. It will not generate alembic migration tree.


For development purposes, we have prepared a command line ``bdc-db db create-schema`` to create
all definitions for ``BDC-Catalog``::

        export SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/bdcdb"
        bdc-db db init
        bdc-db db create-namespaces
        bdc-db db create-extension-postgis
        lccs-db db create-extension-hstore
        bdc-db db create-schema


Creating database definition
----------------------------

**1.** Create a PostgreSQL database and enable the required extensions (`postgis`, `hstore`)::

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/bdcdb" \
        bdc-db db init

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/bdcdb" \
        bdc-db db create-namespaces

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/bdcdb" \
        bdc-db db create-extension-postgis

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/bdcdb" \
        lccs-db db create-extension-hstore


**2.** After that, run ``BDC-DB`` command to prepare the Brazil Data Cube data model::

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/bdcdb" \
        bdc-db alembic upgrade


**3.** The ``BDC-Catalog`` uses `PostgreSQL Triggers <https://www.postgresql.org/docs/12/plpgsql-trigger.html>`_ along database definition. Use the following command line to create default triggers::

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/bdcdb" \
        bdc-db db create-triggers


.. note::

        You can also check the available triggers with command::

                bdc-db db show-triggers

                Available triggers in "bdc_catalog.triggers"
                        -> /home/raphael/devel/github/brazil-data-cube/bdc-catalog/bdc_catalog/triggers/band_metadata_expression.sql
                        -> /home/raphael/devel/github/brazil-data-cube/bdc-catalog/bdc_catalog/triggers/timeline.sql
                        -> /home/raphael/devel/github/brazil-data-cube/bdc-catalog/bdc_catalog/triggers/collection_statistics.sql
                        -> /home/raphael/devel/github/brazil-data-cube/bdc-catalog/bdc_catalog/triggers/collection_tiles.sql



Updating an Existing Data Model
-------------------------------

If you have followed the migration context and would like to upgrade to the latest module migration,
use the following command::

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/bdcdb" \
        bdc-db alembic upgrade


Updating the Migration Scripts
------------------------------

Whenever you made change in a model, (or create a new model file and register with entry point ``bdc_db.models``,
you should generate a new revision and commit these changes into versioning control system (Git).
Use the following command to generate migration changes::

        SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/bdcdb" \
        bdc-db alembic revision "my revision" --branch=bdc_catalog


.. note::

        Make sure to pass ``--branch=bdc_catalog`` in order to generate the alembic migration into
        the same ``BDC-Catalog`` branch tree.


Initial Data
------------

.. note::

    For this step, you will need to install few extra libraries::

        pip3 install -e .[geo]

    It will inject ``Shapely`` into virtual libraries.


We have prepared a minimal command line to insert collections into database.
Please, refer to :doc:`cli` for further details.

You can load a initial data of sentinel-2 using the command line::

    SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/bdcdb" \
    bdc-catalog load-data --ifile examples/fixtures/sentinel-2.json


The following collection ``S2_L1C-1`` will be loaded::

    Collection S2_L1C-1 created
    -> Creating Item S2A_MSIL1C_20151122T132122_N0204_R038_T23LMF_20151122T132134
    - Total 1 items created.

