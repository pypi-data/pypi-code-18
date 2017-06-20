# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 09:52:13 2017

@author: 50063023
"""


from setuptools import setup,find_packages

setup(name='multichain',
      version='0.1.0',
      description='Pure Python wrapper for multichain cli',
      url='https://github.com/edunuke/multichain',
      author='edunuke',
      author_email='eduardo.perez@banistmo.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      package_data={
        'multichain': ['source/*'],
        }
    )