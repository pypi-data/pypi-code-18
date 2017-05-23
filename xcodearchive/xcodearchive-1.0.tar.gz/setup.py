#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/23 下午5:03
# @Author  : 袁平华
# @Site    : 
# @File    : setup.py
# @Software: PyCharm Community Edition


import os

from setuptools import setup, find_packages


def fread(fname):
    filepath = os.path.join (os.path.dirname (__file__), fname)
    with open (filepath, 'r') as fp:
        return fp.read ( )


setup (
    name='xcodearchive',
    version='1.0',
    packages=find_packages ( ),
    author='yuanping',
    author_email='yuanpinghua@yeah.net',
    license='MIT',
    entry_points={
        'console_scripts': [
            'xcodearchive = xcodearchive.xcodetool:main']
    },
)
