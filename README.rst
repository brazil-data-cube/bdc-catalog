..
    This file is part of Brazil Data Cube Database module.
    Copyright (C) 2019 INPE.

    Brazil Data Cube Database Module is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


================================
Brazil Data Cube Database module
================================

.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com/brazil-data-cube/bdc-db/blob/master/LICENSE
        :alt: Software License

.. image:: https://readthedocs.org/projects/bdc-db/badge/?version=b-0.2
        :target: https://bdc-db.readthedocs.io/en/b-0.2/
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/lifecycle-experimental-orange.svg
        :target: https://www.tidyverse.org/lifecycle/#experimental
        :alt: Software Life Cycle

.. image:: https://img.shields.io/github/tag/brazil-data-cube/bdc-db.svg
        :target: https://github.com/brazil-data-cube/bdc-db/releases
        :alt: Release

.. image:: https://badges.gitter.im/brazil-data-cube/community.png
        :target: https://gitter.im/brazil-data-cube/community#
        :alt: Join the chat


.. role:: raw-html(raw)
    :format: html


:raw-html:`<br />`
This is the storage module for the Brazil Data Cube catalog metadata tables. The module relies on SQLAlchemy and Flask related packages in order to store and retrieve data items related to the catalog. All the imagery collections are recorded in tables according to the following schema:

.. image:: https://github.com/brazil-data-cube/bdc-db/raw/b-0.2/doc/model/db-schema.png
        :target: https://github.com/brazil-data-cube/bdc-db/tree/b-0.2/doc/model
        :width: 90%
        :alt: Database Schema


:raw-html:`<br />`
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
    Copyright (C) 2019 INPE.

    Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.