#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import itertools
from setuptools import setup, find_packages


def parse_requirements(requirement_file):
    with open(os.path.join('requirements', requirement_file)) as f:
        return list(filter(None, (l.strip() for l in f.readlines())))


with open('README.rst') as readme_file:
    README = readme_file.read()

extras = {}
for _extra_filename in os.listdir(os.path.join('requirements', 'extras')):
    extra_name = _extra_filename.split('.')[0]
    extras[extra_name] = parse_requirements(os.path.join('extras', _extra_filename))

extras['all'] = list(itertools.chain(*extras.values()))

setup(
    name='roundhouse',
    description="Convert many serialization formats to many formats",
    long_description=README,
    author="Nick Allen",
    author_email='nick.allen.cse@gmail.com',
    url='https://github.com/nick-allen/python-roundhouse',
    packages=find_packages(include=['roundhouse']),
    setup_requires=[
        'setuptools_scm',
        'pytest-runner'
    ],
    use_scm_version=True,
    entry_points={
        'console_scripts': [
            'rh=roundhouse.cli:main'
        ],
        'roundhouse': [
            'contrib_serializers=roundhouse.contrib.serializers'
        ]
    },
    include_package_data=True,
    install_requires=parse_requirements('base.txt'),
    extras_require=extras,
    license="MIT license",
    zip_safe=False,
    keywords='roundhouse',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=parse_requirements('tests.txt')
)
