# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='sancomp',
    version='1.2b8',
    url='https://github.com/douglaskorvo/sancomp',
    license='GPL 3.0',
    author='Douglas Rodrigues',
    author_email='douglas.souza85@gmail.com',
    keywords='sandwich structures analysis software',
    description=u'Sandwich Structures Analysis Software',
    packages=['sancomp','sancomp/image/'],
    install_requires=['numpy >=1.11.2'],
)