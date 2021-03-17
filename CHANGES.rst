..
    This file is part of BDC-Catalog.
    Copyright (C) 2019-2020 INPE.

    BDC-Catalog is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


=======
Changes
=======


Version 0.8.1 (2021-03-17)
--------------------------

- Upgrade BDC-DB dependency to 0.4.3 to keep SQLAlchemy in version 1.3 until SQLAlchemyUtils is updated for SQLAlchemy 1.4. (`#150 <https://github.com/brazil-data-cube/bdc-catalog/issues/150>`_).


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
