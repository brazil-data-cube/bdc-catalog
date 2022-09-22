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


Installation
============


Development installation
------------------------


Pre-Requirements
++++++++++++++++


The ``Brazil Data Cube Catalog`` (``BDC-Catalog``) depends essentially on:

- `BDC-DB <https://bdc-db.readthedocs.io/en/latest/>`_: a database management extension for Brazil Data Cube Applications and Services.

- `LCCS-DB <https://lccs-db.readthedocs.io/en/latest/>`_: the underlying Land Cover Classification System database model.

- `Flask-SQLAlchemy <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>`_: an extension for `Flask <http://flask.pocoo.org/>`_ that adds support for `SQLAlchemy <https://www.sqlalchemy.org/>`_ in applications.

- `Flask-Alembic <https://flask-alembic.readthedocs.io/en/stable/>`_: an extension that provides a configurable `Alembic <https://alembic.sqlalchemy.org/en/latest/>`_ migration environment around a Flask-SQLAlchemy database.

- `GeoAlchemy <https://geoalchemy-2.readthedocs.io/en/latest/>`_: an extension for SQLAlchemy for working with spatial databases.

- `py-multihash <https://multihash.readthedocs.io/en/latest/>`_: the Multihash Implementation in Python.


Clone the software repository
+++++++++++++++++++++++++++++


Use ``git`` to clone the software repository::

    git clone https://github.com/brazil-data-cube/bdc-catalog.git


Install BDC-Catalog in Development Mode
+++++++++++++++++++++++++++++++++++++++


Go to the source code folder::

    cd bdc-catalog


Install in development mode::

    pip3 install -e .[all]


.. note::

    If you want to create a new *Python Virtual Environment*, please, follow this instruction:

    *1.* Create a new virtual environment linked to Python 3.7::

        python3.7 -m venv venv


    **2.** Activate the new environment::

        source venv/bin/activate


    **3.** Update pip and setuptools::

        pip3 install --upgrade pip

        pip3 install --upgrade setuptools


Build the Documentation
+++++++++++++++++++++++


You can generate the documentation based on Sphinx with the following command::

    python setup.py build_sphinx


The above command will generate the documentation in HTML and it will place it under:

.. code-block:: shell

    doc/sphinx/_build/html/


The above command will generate the documentation in HTML and it will place it under::

    docs/sphinx/_build/html/


You can open the above documentation in your favorite browser, as::

    firefox docs/sphinx/_build/html/index.html

