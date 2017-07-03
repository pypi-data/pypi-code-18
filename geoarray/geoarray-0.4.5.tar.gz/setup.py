#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy', 'matplotlib', 'six', 'gdal', 'shapely', 'geopandas', 'dill', 'mpld3', 'geojson', 'folium', 'holoviews'
    #'py_tools_ds' # pip install git+https://gitext.gfz-potsdam.de/danschef/py_tools_ds.git
]

test_requirements = ["coverage"]

setup(
    name='geoarray',
    version='0.4.5',
    description="Fast Python interface for geodata - either on disk or in memory.",
    long_description=readme + '\n\n' + history,
    author="Daniel Scheffler",
    author_email='danschef@gfz-potsdam.de',
    url='https://gitext.gfz-potsdam.de/danschef/geoarray',
    packages=find_packages(), # searches for packages with an __init__.py and returns them as properly formatted list
    package_dir={'geoarray':
                 'geoarray'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords=['geoarray', 'geoprocessing', 'gdal', 'numpy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
