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


=======
Changes
=======

Version 1.0.2 (2023-05-12)
--------------------------

- Fix trigger related collection tiles, ensure JSON concatenation `#193 <https://github.com/brazil-data-cube/bdc-catalog/issues/193>`_.
- Alter JSONB fields entities with ``server_default`` values in tables ``bdc.collections`` and ``bdc.items`` `#193 <https://github.com/brazil-data-cube/bdc-catalog/issues/193>`_.


Version 1.0.1 (2022-12-06)
--------------------------

- Remove integration with lccs-db `#187 <https://github.com/brazil-data-cube/bdc-catalog/issues/187>`_.
- Improve performance on items retrieval
- Fix migration 0.8 - 1.0 related bands metadata ``null`` entry `#189 <https://github.com/brazil-data-cube/bdc-catalog/issues/1189>`_.


Version 1.0.0 (2022-09-22)
--------------------------

- Change LICENSE to GPL v3
- Add command line to manage initial collection data
- Add method utility in ``Item.add_asset`` to make easy way to follow STAC Spec Item Asset. `#179 <https://github.com/brazil-data-cube/bdc-catalog/issues/179>`_.


Version 1.0.0-alpha3 (2022-09-06)
---------------------------------

- Change way to manage control to collections: use roles instead bool flag `#168 <https://github.com/brazil-data-cube/bdc-catalog/issues/168>`_.
- Review static checking: import orders
- Update docs - model png and schema.


Version 1.0.0-alpha2 (2022-09-01)
---------------------------------

- Fix documentation RUNNING.rst
- Fix migration conflict with LCCS-DB instance `#169 <https://github.com/brazil-data-cube/bdc-catalog/issues/169>`_.


Version 1.0.0-alpha1 (2022-07-21)
---------------------------------

- Add authorization control to items `#78 <https://github.com/brazil-data-cube/bdc-catalog/issues/78>`_.
- Review JSONSchemas for collection metadata - instrument key `#68 <https://github.com/brazil-data-cube/bdc-catalog/issues/68>`_.
- Use JSONSchemas to validate any JSONB field in bdc-catalog
- Fix timeline trigger related item end_date `#159 <https://github.com/brazil-data-cube/bdc-catalog/issues/159>`_.
- Review field names for v1.0 `#140 <https://github.com/brazil-data-cube/bdc-catalog/issues/140>`_.
- Review version property - use float/string instead int `#144 <https://github.com/brazil-data-cube/bdc-catalog/issues/144>`_.
- Add new fields for 1.0 - properties according STAC and srid `#157 <https://github.com/brazil-data-cube/bdc-catalog/issues/157>`_.


Version 0.8.2 (2022-03-25)
--------------------------

- Fix dependency related git protocol deprecation (`#161 <https://github.com/brazil-data-cube/bdc-catalog/issues/161>`_).
- Add helper utility to deal with WKB geometries.


Version 0.8.1 (2021-03-17)
--------------------------

- Upgrade BDC-DB dependency to 0.4.3 to keep SQLAlchemy in version 1.3 until SQLAlchemyUtils is updated for SQLAlchemy 1.4. (`#150 <https://github.com/brazil-data-cube/bdc-catalog/issues/150>`_).

- Fix default database schema "bdc" when creating a new GridRefSys (`#148 <https://github.com/brazil-data-cube/bdc-catalog/issues/148>`_).

- Fix migration relation with LCCS-DB (`#147 <https://github.com/brazil-data-cube/bdc-catalog/issues/147>`_).


Version 0.8.0 (2021-01-07)
--------------------------

- Integrate the catalog data model with LCCS data model (`#45 <https://github.com/brazil-data-cube/bdc-catalog/issues/45>`_, `#131 <https://github.com/brazil-data-cube/bdc-catalog/issues/131>`_).

- Add prefix bdc to assets metadata specific to Brazil Data Cube (`#115 <https://github.com/brazil-data-cube/bdc-catalog/issues/115>`_).

- ``check_sum`` enhancement: (`#134 <https://github.com/brazil-data-cube/bdc-catalog/issues/134>`_, `#135 <https://github.com/brazil-data-cube/bdc-catalog/issues/135>`_).

- Improve Sphinx documentation (`#27 <https://github.com/brazil-data-cube/bdc-catalog/issues/27>`_, `#133 <https://github.com/brazil-data-cube/bdc-catalog/issues/133>`_).



Version 0.6.4 (2020-11-30)
--------------------------


- Added new collection types: ``classification`` and ``mosaic`` (`#127 <https://github.com/brazil-data-cube/bdc-catalog/pull/127>`_)



Version 0.6.3 (2020-11-05)
--------------------------


- Bug fix: update GeoAlchemy version dependency (`#118 <https://github.com/brazil-data-cube/bdc-catalog/issues/118>`_)


Version 0.6.2 (2020-09-20)
--------------------------


- Bug fix: trigger update_collection (`#116 <https://github.com/brazil-data-cube/bdc-catalog/issues/116>`_)


Version 0.6.1 (2020-09-09)
--------------------------


- Bug fix: fix grid CRS retrieval (`#112 <https://github.com/brazil-data-cube/bdc-catalog/issues/112>`_)



Version 0.6.0 (2020-09-01)
--------------------------


- Data model improvements:

  - Added a ``timeline`` table to speedup data cube temporal dimension queries.

  - Added database triggers to pre-compute the timeline, extent and data range of image collections.

  - Added ``band_src`` table to track the origin of data bands.


- New features:

  - Add utility functions for dealing with file check-sum and multihash format.


- Code improvement:

  - Timestamp columns use database ``now()`` function.

  - Better support for the PostGIS table ``spatial_ref_sys``.


- Improved usage documentation.


Version 0.4.1 (2020-08-31)
--------------------------


- Minor fixes:

  - Create Grid geometry table as lowered case. `#83 <https://github.com/brazil-data-cube/bdc-catalog/issues/83>`_

  - Add cascade in the quicklook table. `#80 <https://github.com/brazil-data-cube/bdc-catalog/issues/80>`_

  - Fix bug in get_geom_table (grid_ref_sys). `#79 <https://github.com/brazil-data-cube/bdc-catalog/issues/79>`_


Version 0.4.0 (2020-08-18)
--------------------------


- Improved data model:

  - Improved ``collections`` table:

    - field for the dataset title.
    - instrument metadata field.
    - visibility field for public or private collections.
    - DataCite Kernel-4 metadata for publication and citation of research data.
    - general JSON metadata field
    - provider association.
    - collection versioning.
    - collection provenance/lineage: datasets used to create collection, lineage (successor and predecessor), algorithm processors.

  - Table ``items``:

    - ``Assets`` moved to a JSON column.
    - ``min_convex_hull`` column besides the footprint geometry.
    - track application that recorded the item.
    - track the data provider of the collection.
    - Assets now have a checksum field and the number of bytes field.

  - Table ``bands``:

    - metadata field as a JSON column.

  - Added table ``quicklook``.

  - Added table ``applications``.

  - Added collection providers table (tables: ``providers``, ``collection_providers``).

- Reviewed Sphinx documentation.

- Use of `BDC-DB Extension Version 0.2.0 <https://github.com/brazil-data-cube/bdc-db>`_.


Version 0.2.1 (2020-02-20)
--------------------------


- Added fixtures commands to the CLI.

- Added new test cases.


Version 0.2.0 (2020-02-18)
--------------------------


- First experimental version.

- Metadata support for: Imagery Collections, Data Cubes and Grid Systems.

- Documentation system based on Sphinx.

- Documentation integrated to ``Read the Docs``.

- Package support through Setuptools.

- Installation and use instructions.

- Schema versioning through Flask-Migrate.

- Source code versioning based on `Semantic Versioning 2.0.0 <https://semver.org/>`_.

- License: `MIT <https://raw.githubusercontent.com/brazil-data-cube/bdc-db/b-0.2/LICENSE>`_.
