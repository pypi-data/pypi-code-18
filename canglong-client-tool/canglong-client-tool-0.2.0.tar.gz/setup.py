#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author: MapzChen
# Email: 61966578@qq.com

from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="canglong-client-tool",
    version="0.2.0",
    author="Mapz Chen",
    author_email="61966578@qq.com",
    description="A data parsing tool for my project",
    long_description=open("README.rst").read(),
    license="MIT",
    url="http://git.oschina.net/Mapz/canglong-client-tool",
    packages=['client_data_tool'],
    install_requires=[
        "xlrd",
        "paramiko",
    ],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)