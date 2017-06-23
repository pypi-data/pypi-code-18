"""Deprecated. Use postgis package instead."""

from setuptools import setup, find_packages


print("\n\nDEPRECATED! Use `postgis>=1.0.0` package directly instead.\n\n")

VERSION = (0, 4, 0)

setup(
    name='psycopg-postgis',
    version=".".join(map(str, VERSION)),
    description=__doc__,
    long_description="Deprecated. Use postgis package instead.",
    url="https://github.com/yohanboniface/python-postgis",
    author='Yohan Boniface',
    author_email='yohan.boniface@data.gouv.fr',
    license='WTFPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 7 - Inactive',

        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='psycopg postgis gis asyncpg',
    packages=find_packages(exclude=['tests']),
    install_requires=['postgis'],
)
