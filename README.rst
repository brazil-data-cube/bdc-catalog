..
    This file is part of BDC-Catalog.
    Copyright (C) 2019-2020 INPE.

    BDC-Catalog is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


=======================================
Brazil Data Cube Image Metadata Catalog
=======================================


.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com/brazil-data-cube/bdc-db/blob/master/LICENSE
        :alt: Software License


.. image:: https://travis-ci.org/brazil-data-cube/bdc-catalog.svg?branch=master
        :target: https://travis-ci.org/brazil-data-cube/bdc-catalog
        :alt: Build Status


.. image:: https://coveralls.io/repos/github/brazil-data-cube/bdc-catalog/badge.svg?branch=master
        :target: https://coveralls.io/github/brazil-data-cube/bdc-catalog?branch=master
        :alt: Code Coverage Test


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


BDC-Catalog is an image metadata storage module for Earth Observation imagery. The module handles Earth Observation image collections and data cubes. The following diagram shows the tables used to store the metadata and their relationships:


.. image:: https://github.com/brazil-data-cube/bdc-catalog/raw/master/docs/model/db-schema.png
        :target: https://github.com/brazil-data-cube/bdc-catalog/tree/master/docs/model
        :width: 90%
        :alt: Database Schema


In the above diagram, for every column of type JSON there is a specific JSONSchema. See the folder `bdc_catalog/jsonschemas <https://github.com/brazil-data-cube/bdc-catalog/tree/master/bdc_catalog/jsonschemas>`_.


This is the base package for other softwares in the Brazil Data Cube project. For instance, the `Brazil Data Cube Spatiotemporal Asset Catalog implementation <https://github.com/brazil-data-cube/bdc-stac>`_ and the `Brazil Data Cube Collection Builder <https://github.com/brazil-data-cube/bdc-collection-builder>`_ rely on it.


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