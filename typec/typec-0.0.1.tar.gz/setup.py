# -*- coding: utf-8 -*-
#
# This file is part of the typec library
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

import os
import sys
from setuptools import setup

# make sure we use qredis from the source
_this_dir = os.path.dirname(__file__)
sys.path.insert(0, _this_dir)

import typec

requirements = [
]

with open(os.path.join(_this_dir, 'README.rst')) as f:
    readme = f.read()

setup(
    name='typec',
    version=typec.__version__,
    description="typechecking library",
    long_description=readme,
    author="Tiago Coutinho",
    author_email='coutinhotiago@gmail.com',
    url='https://github.com/tiagocoutinho/typec',
    packages=['typec'],
    install_requires=requirements,
    zip_safe=False,
    keywords='typing',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

