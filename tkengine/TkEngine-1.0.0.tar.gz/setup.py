from setuptools import setup

setup(
	name='TkEngine',
	version='1.0.0',
	description='A GUI and Game engine with pyglet.',
	url='https://github.com/tlebrize/TkEngine',
	author='tlebrize',
	author_email='tlebrize@student.42.fr',
	license='BEER-WARE LICENSE (https://en.wikipedia.org/wiki/Beerware)',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Programming Language :: Python :: 3.6',
	],
	keywords='engine pyglet python python3 gui',
	packages=['tkengine'],
	install_requires=['pyglet']
)
