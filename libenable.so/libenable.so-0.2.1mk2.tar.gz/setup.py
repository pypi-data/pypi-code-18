from setuptools import setup, find_packages

def format(input, start = 0):
	result = ''
	indent = False
	count = 0

	with open(input, 'r') as file:
		for line in file:
			if count > start:
				if line[:1] == '\t' and not indent:
					indent = True
					result += '::\n\n'

				if line[:1].isalnum() and indent:
					indent = False

				result += line.replace('> ', '\t')
			count += 1

	return result

blurb = ('libenable.so is a Python module designed to enable access to'
	' different protected domains\n'
)

setup(
	name = 'libenable.so',
	version = '0.2.1',
	author = 'Justin Willis',
	author_email = 'sirJustin.Willis@gmail.com',
	packages = find_packages(),
	include_package_data = True,
	zip_safe = False,
	url = 'https://bitbucket.org/bkvaluemeal/libenable.so',
	license = 'ISC License',
	description = 'A Python module for enabling access to different'\
		' protected domains',
	long_description = blurb + format('README.md', 3),
	entry_points = {
		'console_scripts': [
			'libenable = libenable.__main__:main'
		]
	},
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Framework :: Flask',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: ISC License (ISCL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Topic :: Other/Nonlisted Topic'
	],
	keywords = 'captcha',
	install_requires = [
		'caboodle',
		'flask',
		'flask_bootstrap',
		'flask_restful',
		'requests'
	]
)
