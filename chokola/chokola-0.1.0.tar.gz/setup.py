#!/usr/bin/env python

from setuptools import setup

__version__ = '0.1.0'

setup(
    name='chokola',
    version=__version__,
    description='YAML to HTML Table',
    author='Noel Martignoni',
    author_email='noel@martignoni.fr',
    url='https://gitlab.com/chokola/chokola',
    scripts = ['scripts/chokola'],
    install_requires=['future', 'pyyaml'],
    packages = ['chokola'],
)
