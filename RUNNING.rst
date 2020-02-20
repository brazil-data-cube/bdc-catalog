..
    This file is part of Brazil Data Cube Database module.
    Copyright (C) 2019 INPE.

    Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Running BDC-DB in the Command Line
==================================


Creating the Brazil Data Cube data model
----------------------------------------

**1.** Create a PostgreSQL database and enable the PostGIS extension:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db db create-db


**2.** After that, run Flask-Migrate command to prepare the Brazil Data Cube data model:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db db upgrade


**3.** Load default fixtures of Brazil Data Cube data model:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db fixtures init


Updating an Existing Data Model
-------------------------------

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db db upgrade


Updating the Migration Scripts
------------------------------

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db db migrate
