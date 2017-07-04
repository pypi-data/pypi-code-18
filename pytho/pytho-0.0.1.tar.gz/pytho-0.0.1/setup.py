#!/usr/bin/env python3

from setuptools import setup

setup(
    name='pytho',
    version='0.0.1',
    description='Library for processing Vietnamese poetry',
    author='Viet Hung Nguyen',
    author_email='hvn@familug.org',
    py_modules=['pytho'],
    url='https://github.com/hvnsweeting/pytho',
    entry_points='''[console_scripts]
        pytho=pytho:cli
    '''
)
