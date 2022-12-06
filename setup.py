#
# This file is part of BDC-Catalog.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Image catalog extension for Brazil Data Cube applications and services."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

history = open('CHANGES.rst').read()

docs_require = [
    'Sphinx>=2.2',
    'sphinx_rtd_theme',
    'sphinx-copybutton',
    'sphinx-tabs',
]

tests_require = [
    'coverage>=4.5',
    'pytest>=5.2',
    'pytest-cov>=2.8',
    'pytest-pep8>=1.0',
    'pydocstyle>=4.0',
    'shapely>=1.7,<2',
    'isort>4.3',
    'check-manifest>=0.40',
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
    'geo': [
        'Shapely>=1.8'
    ]
}

extras_require['all'] = [req for _, reqs in extras_require.items() for req in reqs]

setup_requires = [
    'pytest-runner>=5.2',
]

install_requires = [
    'Flask>=1.1.0',
    'Flask-SQLAlchemy>=2.4.0',
    'Flask-Alembic>=2.0.0',
    'GeoAlchemy2>=0.8.4',
    'py-multihash>=2,<3',
    'bdc-db @ git+https://github.com/brazil-data-cube/bdc-db@v0.6.3',
]

packages = find_packages()
# Remove warning for PEP
packages += ['bdc_catalog.alembic',
             'bdc_catalog.triggers']

g = {}
with open(os.path.join('bdc_catalog', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='bdc-catalog',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords=['database', 'postgresql', 'image collection', 'Earth Observation Data Cubes'],
    license='GPLv3',
    author='Brazil Data Cube Team',
    author_email='brazildatacube@inpe.br',
    url='https://github.com/brazil-data-cube/bdc-catalog',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'bdc_db.alembic': [
            'bdc_catalog = bdc_catalog:alembic'
        ],
        'bdc_db.models': [
            'bdc_catalog = bdc_catalog.models'
        ],
        'bdc_db.triggers': [
            'bdc-catalog = bdc_catalog.triggers'
        ],
        'bdc_db.namespaces': [
            'bdc_catalog = bdc_catalog.config:BDC_CATALOG_SCHEMA'
        ],
        'bdc.schemas': [
            'bdc_catalog = bdc_catalog.jsonschemas'
        ],
        'console_scripts': [
            'bdc-catalog = bdc_catalog.cli:cli'
        ]
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 3 - Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GPL v3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)
