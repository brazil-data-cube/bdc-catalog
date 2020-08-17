..
    This file is part of BDC-Catalog.
    Copyright (C) 2019-2020 INPE.

    BDC-Catalog is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


================================
Brazil Data Cube Database module
================================


.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com/brazil-data-cube/bdc-db/blob/master/LICENSE
        :alt: Software License


.. image:: https://readthedocs.org/projects/bdc-catalog/badge/?version=latest
        :target: https://bdc-catalog.readthedocs.io/en/latest/
        :alt: Documentation Status


.. image:: https://img.shields.io/badge/lifecycle-experimental-orange.svg
        :target: https://www.tidyverse.org/lifecycle/#experimental
        :alt: Software Life Cycle


.. image:: https://img.shields.io/github/tag/brazil-data-cube/bdc-catalog.svg
        :target: https://github.com/brazil-data-cube/bdc-catalog/releases
        :alt: Release


.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord


About
=====


This is the storage module for the Brazil Data Cube catalog metadata tables. The module relies on `Flask-SQLAlchemy <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>`_ and related packages in order to store and retrieve data items related to the catalog. All the imagery collections are recorded in tables according to the following schema:


.. image:: https://github.com/brazil-data-cube/bdc-db/raw/master/doc/model/db-schema.png
        :target: https://github.com/brazil-data-cube/bdc-db/tree/master/doc/model
        :width: 90%
        :alt: Database Schema


Therefore, this is the base package for other softwares in the Brazil Data Cube project. For instance, the `Brazil Data Cube Spatiotemporal Asset Catalog implementaion <https://github.com/brazil-data-cube/bdc-stac>`_  relies on it. The `Brazil Data Cube Collection Builder <https://github.com/brazil-data-cube/bdc-collection-builder>`_ is another system that relies on this module.


Installation
============


See `INSTALL.rst <./INSTALL.rst>`_.


Running
=======


See `RUNNING.rst <./RUNNING.rst>`_.


Developer Documentation
=======================


See https://bdc-db.readthedocs.io/en/latest/


License
=======

.. admonition::
    Copyright (C) 2019-2020 INPE.

    Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.