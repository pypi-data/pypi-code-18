#!/usr/bin/env python
import os

from setuptools import find_packages, setup

root = os.path.abspath(os.path.dirname(__file__))

setup(
    name='rimradio',
    version='0.1.0',
    description='Simple GTK stream radio player',
    author='Marcin Rim',
    author_email='rimek@poczta.fm',
    url='https://github.com/rimek/radio-gtk',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'rimradio': ('icons/play.png', 'icons/stop.png'),
    },
    zip_safe=False,
    install_requires=[
        'vext',
        'vext.gi',
        'requests',
    ],
    scripts=['bin/rimradio'],
    test_suite='tests',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
