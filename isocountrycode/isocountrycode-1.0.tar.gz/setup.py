#!/usr/bin/env python
"""
ISO Country Codes
----------------

Provides enums for ISO Country Codes
"""
import sys
from setuptools import setup

install_requires = []
if sys.version_info < (3, 4):
    install_requires.append("enum==0.4.6")

setup(
    name='isocountrycode',
    version='1.0',
    url='http://github.com/geoffreybauduin/python-isocountrycode',
    license='MIT',
    author='Geoffrey Bauduin',
    author_email='bauduin.geo@gmail.com',
    maintainer='Geoffrey Bauduin',
    maintainer_email='bauduin.geo@gmail.com',
    description="Provides enums for ISO representation of countries",
    long_description=__doc__,
    packages=['isocountrycode'],
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)