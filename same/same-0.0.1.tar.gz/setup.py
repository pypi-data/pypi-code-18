#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2017 The Authors. All Rights Reserved.
# License: MIT.
# Author: acrazing <joking.young@gmail.com>.
# File: setup.
from setuptools import setup
from same.Client import version

with open('./README.md', encoding='utf8') as f:
    desc = f.read()

with open('./requirements.txt') as f:
    requires = [r.split('=', 1)[0] for r in f.read().split('\n') if r]

setup(
    name='same',
    version=version,
    description='same shell client',
    url='https://github.com/acrazing/same-api',
    author='acrazing',
    author_email='joking.young@gmail.com',
    license='MIT',
    keywords='same client api',
    long_description=desc,
    install_requires=requires,
    packages=['same'],
    entry_points={
        'console_scripts': 'same = same.cli:same',
    },
)
