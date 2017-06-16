#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Setup script for csft """
import codecs
import sys
from os.path import abspath, dirname, join

from setuptools import find_packages, setup

import csft

VER = sys.version
HERE = abspath(dirname(__file__))


def _read(rel_path):
    path = join(HERE, rel_path)
    with codecs.open(path, "rb", "utf-8") as file_obj:
        return file_obj.read()


REQUIRES = [
    'pandas >= 0.20.1',
]

if VER >= '3.0' and VER < '3.2':
    REQUIRES.append('argparse >= 1.4.0')

if VER < '3.4':
    REQUIRES.append('pathlib >= 1.0.1')

if VER < '3.5':
    REQUIRES.append('scandir >= 1.5')

setup(
    name=csft.__name__,
    version=csft.__version__,
    description='Count Sizes of File Types',
    long_description=_read('README.rst'),
    url=csft.__url__,
    author=csft.__author__,
    author_email=csft.__email__,
    license=csft.__license__,
    packages=find_packages(),
    entry_points={
        'console_scripts': (
            'csft = csft.__main__:main',
        ),
    },
    python_requires='>=2.7',
    install_requires=REQUIRES,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)
