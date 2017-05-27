#!/usr/bin/env python

from distutils.core import setup

setup(
    name='dojo-mysql',
    version='0.0.8',
    description='Dojo source and sink adapters for MySQL connections.',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=['dojo_mysql', ],
    install_requires=[
      'dojo',
      'mysqlclient'
    ]
)
