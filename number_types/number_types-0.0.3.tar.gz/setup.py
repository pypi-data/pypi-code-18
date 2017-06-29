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
    from number_types import __version__
finally:
    sys.path.pop(0)

with open(path.join(__dir__, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def test_suite():
    test_loader = unittest.TestLoader()
    return test_loader.discover(__dir__, pattern='tests*.py')

setup_args = dict(
    name='number_types',

    version=__version__,

    description='Various number types for Python',
    long_description=long_description,

    url='https://github.com/MitalAshok/number_types',

    author='MitalAshok',
    author_email='mital.vaja@googlemail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    platforms=['any'],

    keywords=['types', 'number', 'coordinates', 'complex'],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[],
    extras_require={},
    entry_points={},

    test_suite='setup.test_suite'
)


setup(**setup_args)
