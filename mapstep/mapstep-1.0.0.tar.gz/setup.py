from setuptools import setup, find_packages
from os import path

import mapstep  # for entry_point


VERSION = '1.0.0'

here = path.abspath(path.dirname(__file__))


setup(
    name='mapstep',
    version=VERSION,
    description="A webapp to put some markers with a description on a leaflet map.",
    long_description=open(path.join(here, 'README.md')).read(),
    url='https://github.com/fspot/mapstep',
    author='fspot',
    author_email='fred@fspot.org',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask>=0.12.2', 'flask-cors', 'tinydb', 'waitress'],
    entry_points = {
        'console_scripts': [
            'mapstep = mapstep.mapstep:main',
        ],
    },
    license='BSD',
)
