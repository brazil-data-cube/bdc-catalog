..
    This file is part of BDC-Catalog.
    Copyright (C) 2019-2020 INPE.

    BDC-Catalog is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


=======
Changes
=======


Version 0.4.0
-------------


Released 2020-08-18


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


Version 0.2.1
-------------


Released 2020-02-20

- Added fixtures commands to the CLI.

- Added new test cases.


Version 0.2.0
-------------


Released 2020-02-18


- First experimental version.

- Metadata support for: Imagery Collections, Data Cubes and Grid Systems.

- Documentation system based on Sphinx.

- Documentation integrated to ``Read the Docs``.

- Package support through Setuptools.

- Installation and use instructions.

- Schema versioning through Flask-Migrate.

- Source code versioning based on `Semantic Versioning 2.0.0 <https://semver.org/>`_.

- License: `MIT <https://raw.githubusercontent.com/brazil-data-cube/bdc-db/b-0.2/LICENSE>`_.
