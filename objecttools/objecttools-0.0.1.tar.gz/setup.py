#!/usr/bin/env python

from setuptools import setup, find_packages

import sys
import unittest

from os import path
from codecs import open


__dir__ = path.abspath(path.dirname(__file__))

# To prevent a redundant __version__, import it from the packages
sys.path.insert(0, __dir__)

try:
    from objecttools import __version__, __author__, __email__
finally:
    sys.path.pop(0)

with open(path.join(__dir__, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def test_suite():
    test_loader = unittest.TestLoader()
    return test_loader.discover(path.join(__dir__, 'tests'), pattern='test*.py')

setup_args = dict(
    name='objecttools',

    version=__version__,

    description='Various tools for working with objects and classes in Python',
    long_description=long_description,

    url='https://github.com/MitalAshok/objecttools',

    author=__author__,
    author_email=__email__,

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    platforms=['any'],

    keywords=['library', 'cached', 'properties', 'singletons'],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[],
    extras_require={},
    entry_points={},

    test_suite='setup.test_suite'
)


setup(**setup_args)
