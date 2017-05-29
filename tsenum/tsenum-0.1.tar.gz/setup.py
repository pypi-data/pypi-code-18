# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import tsenum, sys

long_description=open("README.md", "r").read(4096)

setup(
	name=tsenum.prog,
	version=tsenum.version,
	description=tsenum.description,
	long_description=long_description,
	license=tsenum.license,
	url=tsenum.url,
	
	author=tsenum.author,
	author_email=tsenum.author_mail,

	classifiers = [
		'Development Status :: 5 - Production/Stable',

		'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',

		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',

		'Operating System :: Unix',
		'Operating System :: POSIX :: Linux',
		'Operating System :: Microsoft',

		'Topic :: Utilities',
  ],

	packages=find_packages(),

	entry_points = {
		'console_scripts': [
			'eggsecutable = tsenum.main_func',
		],
	},

	keywords="utils timestamp",
)

# vim: ft=python tabstop=2 shiftwidth=2 noexpandtab :
