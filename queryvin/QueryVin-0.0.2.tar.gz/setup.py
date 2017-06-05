# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='QueryVin',
      version='0.0.2',
      description='query vin information',
      url='https://github.com/fiveddd/QueryVin',
      author='FiveDDD',
      author_email='lhorvce@hotmail.com',
      license='MIT License',
      packages=['QueryVin'],
      install_requires=[
          'requests',
          'lxml',
      ],
      zip_safe=False)
