#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
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
    'coveralls>=1.8',
    'pytest>=5.2',
    'pytest-cov>=2.8',
    'pytest-pep8>=1.0',
    'pydocstyle>=4.0',
    'isort>4.3',
    'check-manifest>=0.40',
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
}

extras_require['all'] = [req for _, reqs in extras_require.items() for req in reqs]

setup_requires = [
    'pytest-runner>=5.2',
]

install_requires = [
    'Flask>=1.1.0',
    'Flask-SQLAlchemy>=2.4.0',
    'Flask-Alembic>=2.0.0',
    'GeoAlchemy2>=0.6.2',
    'SQLAlchemy[postgresql_psycopg2binary]>=1.3.10',
    'SQLAlchemy-Utils>=0.36.0',
    'alembic>=1.4.0',
    'bdc-db @ git+git://github.com/brazil-data-cube/bdc-db@v0.4.0'
]

packages = find_packages()

g = {}
with open(os.path.join('bdc_catalog', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='bdc-catalog',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords=['database', 'postgresq', 'image collection', 'Earth Observation Data Cubes'],
    license='MIT',
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
        'console_scripts': [
            'bdc-catalog = bdc_catalog.cli:cli'
        ],
        'bdc_db.triggers': [
            'bdc-catalog = bdc_catalog.triggers'
        ]
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)
