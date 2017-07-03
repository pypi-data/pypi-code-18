# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

setup(
	name='sancomp',
	version='1.2b11',
	url='https://github.com/douglaskorvo/sancomp',
	license='GPL 3.0',
	author='Douglas Rodrigues',
	author_email='douglas.souza85@gmail.com',
	keywords='sandwich structures analysis software',
	description=u'Sandwich Structures Analysis Software',
	#python_requires='==2.7',
	packages=['sancomp'],
	package_data={'sancomp': ['*.*','image/*.*'],},
	#data_files={'sancomp': ['*.*'],},,
	install_requires=['numpy >=1.11.2'],
)