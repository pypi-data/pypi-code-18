# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="psycopg2-range-overlaps",
    version='1.0.0',
    description="Use & and = on psycopg2 range types.",
    long_description=long_description,
    url="https://bitbucket.org/schinckel/psycopg2-range-overlaps",
    author="Matthew Schinckel",
    author_email="matt@schinckel.net",
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'psycopg2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='runtests.runtests',
)
