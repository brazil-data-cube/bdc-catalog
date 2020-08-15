..
    This file is part of Brazil Data Cube Database module.
    Copyright (C) 2019 INPE.

    Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Installation
============

The ``Brazil Data Cube Catalog`` (``BDC-Catalog``) depends essentially on
`Flask-Alembic <https://flask-alembic.readthedocs.io/en/stable/>`_ and
`Flask-SQLAlchemy <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>`_.
Please, read the instructions below in order to install ``BDC-Catalog``.


Production installation
-----------------------

**Under Development!**


Development installation
------------------------

Clone the software repository:

.. code-block:: shell

        $ git clone https://github.com/brazil-data-cube/bdc-catalog.git


Go to the source code folder:

.. code-block:: shell

        $ cd bdc-catalog


Install in development mode:

.. code-block:: shell

        $ pip3 install -e .[all]


Generate the documentation:

.. code-block:: shell

        $ python setup.py build_sphinx


The above command will generate the documentation in HTML and it will place it under:

.. code-block:: shell

    doc/sphinx/_build/html/
