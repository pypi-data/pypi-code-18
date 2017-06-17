from setuptools import setup

setup(
	name = 'icheckin',
	packages = ['icheckin'],
	install_requires = [
		'requests'
	],
	version = '1.1.0',
	description = 'A console application for Sunway University\'s iCheckin',
	author = 'Marcus Mu',
	author_email = 'chunkhang@gmail.com',
	license = 'UNLICENSE',
	url = 'https://github.com/chunkhang/icheckin',
	keywords = [
		'icheckin', 
		'sunway'
	], 
	classifiers = [
		'Intended Audience :: End Users/Desktop',
		'Programming Language :: Python :: 3 :: Only',
		'Environment :: Console'
	],
	entry_points = {
		'console_scripts': [
			'icheckin=icheckin.icheckin:main'
		]
	}
)