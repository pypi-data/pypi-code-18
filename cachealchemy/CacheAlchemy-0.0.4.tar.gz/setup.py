# coding=utf8

__author__ = 'liming'

from setuptools import setup

setup(name='CacheAlchemy',
      version='0.0.4',
      description='Cache SqlAlchemy entity to memory cache system',
      url='https://github.com/ipconfiger/CacheAlchemy',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      license='MIT License',
      packages=['CacheAlchemy'],
      install_requires=[
          'sqlalchemy',
          'redis',
      ],
      zip_safe=False)
