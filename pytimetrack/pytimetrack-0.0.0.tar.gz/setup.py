#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

#version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split("=")[1].strip().replace("\"", "") for line in open(os.path.join(here,"pytimetrack","__init__.py")) if line.startswith("__version__ = ")),"0.0.0")
print(version)

try:
    with open("README.rst") as f:
        readme = f.read()
except IOError:
    readme = ""

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name        = "pytimetrack",
    version     = version,
    author      = "Yusaku Takano",
    author_email= "takano-yuusaku@ed.tmu.ac.jp",
    license     = "MIT License",
    description = "Track Classification",
    long_description=readme,
    packages=find_packages(),
    url="https://github.com/ty-edelweiss/pycurvature",
    install_requires=_requires_from_file("requirements.txt"),
    classifiers = [
    "Programming Language :: Python :: 3.6",
    "License :: OSI Approved :: MIT License"
    ],
)
