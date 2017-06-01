
from setuptools import setup, find_packages

 
import os
import codecs
setup(

	name='moageet',
	version='1.0.1',
	description='Moageet al salah',
	author='Mansour A Almansour',
	author_email='almansour2345@gmail.com',
	license='GPL-3.0',
	scripts=['moageet.py'],
	install_requires=[
        'python-requests',
        'python-tk',],

	)
    
