#!/usr/bin/env python

from setuptools import find_packages, setup

setup(name='qwertyui',
      version='1.0.1',
      description='Some common Python functions and algorithms',
      author='Przemyslaw Kaminski',
      author_email='cgenie@gmail.com',
      url='https://github.com/CGenie/qwertyui',
      packages=find_packages(exclude=['tests.py'])
)
