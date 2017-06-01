#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='netgard',
    version='0.0.0rc0',
    description='Neuro-realistic neural network',
    author='Edgar Y. Walker',
    author_email='eywalker@bcm.edu',
    url='https://github.com/cajal/netgard',
    packages=find_packages(exclude=[]),
    install_requires=[],
)

