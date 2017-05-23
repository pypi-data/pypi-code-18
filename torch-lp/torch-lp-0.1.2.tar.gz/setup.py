#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
from setuptools import setup, find_packages
import sys


setup(
        name = "torch-lp",
        version = "0.1.2",
        author = "Bingzhe",
        author_email = "wubingzheagent@gmail.com",
        description = "quantization simulation tools for Pytorch",
        long_description = open('torchlp/README.md').read(),
        license="MIT",
        packages=["torchlp"],
        #install_requires=['torch'],
)

