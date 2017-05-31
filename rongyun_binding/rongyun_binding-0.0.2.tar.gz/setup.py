# coding=utf8
__author__ = 'liming'

from setuptools import setup

setup(name='rongyun_binding',
      version='0.0.2',
      description='Integrate instant messaging services into your system',
      url='https://github.com/ipconfiger/rongyun_binding',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      license='GNU GENERAL PUBLIC LICENSE',
      packages=['rongyun_binding'],
      install_requires=[
          'flask','sqlalchemy', 'singleton', 'rongcloud'
      ],
      zip_safe=False)
