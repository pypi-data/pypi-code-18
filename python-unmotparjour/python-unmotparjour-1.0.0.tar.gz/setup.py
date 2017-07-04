
from setuptools import setup

setup(
	name='python-unmotparjour',
	version='1.0.0',
	description='Cool simple Python module to get random words with definition (online-only usage, crawl from "unmotparjour.fr") - French',
	packages=['unmotparjour'],
	url='https://github.com/remaudcorentin-dev/python-unmotparjour',
	author='Corentin Remaud',
	author_email='remaudcorentin.dev@gmail.com',
	license='MIT',
	zip_safe=False,
	install_requires=['bs4'],
	)
