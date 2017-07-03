# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='sancomp',
    version='1.2b9',
    url='https://github.com/douglaskorvo/sancomp',
    license='GPL 3.0',
    author='Douglas Rodrigues',
    author_email='douglas.souza85@gmail.com',
    keywords='sandwich structures analysis software',
    description=u'Sandwich Structures Analysis Software',
    packages=['sancomp'],
	packages_data={
    'sancomp': ['face-elasticidade-poisson.dat','nucleo-elasticidade.dat','sancompt.ui'],
	},
	data_files=[('images', ['image/v1.png','image/sec2.png','image/v0.png','image/v2.png','image/v3.png','image/v4.png','image/v5.png','image/v6.png','image/v7.png','image/beam.png','image/sancomp.ico','image/sancomp.png'])],
    install_requires=['numpy >=1.11.2'],
)