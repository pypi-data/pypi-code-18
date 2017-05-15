#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
from tayne import __version__

def slurp(filename):
    with open(filename) as f:
        return f.read()


setup(name='tayne',
      version=__version__,
      description='companion to entr(1)',
      long_description=slurp('README.rst'),
      url='https://github.com/eddieantonio/tayne',
      author='Eddie Antonio Santos',
      author_email='easantos@ualberta.ca',

      license='ISC',

      packages=find_packages(),
      install_requires=['docopt >= 0.6.0'],
      entry_points={
          'console_scripts': [
              'tayne=tanye.__main__:main'
          ]
      })
