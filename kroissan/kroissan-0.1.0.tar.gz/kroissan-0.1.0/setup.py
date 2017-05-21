#!/usr/bin/env python

from setuptools import setup

__version__ = '0.1.0'

setup(
    name='kroissan',
    version=__version__,
    description='YAML spreadsheet',
    author='Noel Martignoni',
    author_email='noel@martignoni.fr',
    url='https://gitlab.com/kroissan/kroissan',
    scripts = ['scripts/kroissan'],
    install_requires=[],
    packages = ['kroissan'],
)
