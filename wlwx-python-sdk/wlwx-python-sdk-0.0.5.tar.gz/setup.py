#!/usr/bin/python3
# -*- coding:utf-8 -*-
#filename:setup

__author__ = 'zhouzhao'

from setuptools import setup, find_packages

setup(
    name = 'wlwx-python-sdk',
    version = '0.0.5',
    keywords = ('wlwx', 'sdk','python'),
    description = 'The http://www.10690757.com python sdk.',
    license = 'MIT License',
    install_requires = ['requests>=2.9.1'],

    author = 'zhouzhao',
    author_email = '2880987282@qq.com',
    url='http://www.10690757.com',

    packages = find_packages(),
    platforms = 'any',
)