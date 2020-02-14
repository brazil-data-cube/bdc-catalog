#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database moduleis free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Database module"""

import os
from setuptools import find_packages, setup

readme = open('README.rst').read()

history = open('CHANGES.rst').read()

docs_require = [
    'bdc-readthedocs-theme @ git+git://github.com/brazil-data-cube/bdc-readthedocs-theme.git#egg=bdc-readthedocs-theme',
    'Sphinx>=2.2',
]

tests_require = []

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
}

extras_require['all'] = [ req for exts, reqs in extras_require.items() for req in reqs ]

setup_requires = [
]

install_requires = [
    'Flask-Migrate>=2.5.2',
    'Flask-SQLAlchemy>=2.4.1',
    'GeoAlchemy2>=0.6.2',
    'SQLAlchemy[postgresql]>=1.3.10',
    'SQLAlchemy-Utils>=0.34.2',
]

packages = find_packages()

with open(os.path.join('bdc_db', 'version.py'), 'rt') as fp:
    g = {}
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='bdc-db',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='Brazil Data Cube Database Module',
    license='MIT',
    author='INPE',
    author_email='gribeiro@dpi.inpe.br',
    url='https://github.com/brazil-data-cube/bdc-db.py',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'bdc-db = bdc_db.cli:cli'
        ]
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
