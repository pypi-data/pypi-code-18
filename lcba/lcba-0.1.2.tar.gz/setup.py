#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys
import  os

setup(
    name="lcba",
    version="0.1.2",
    author="tory you",
    author_email="feiy1@jumei.com",
    description="lint clean android and compress android resources",
    long_description="""
    LCBA is a fineresource project use lint delete unUsed file and value. And this we will compress the picture for
    save the disk.
    """,
    license="MIT",
    url="https://www.baidu.com",
    packages=['lcba'],
    install_requires=[
        "lxml",
        # lxml_requirement
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)