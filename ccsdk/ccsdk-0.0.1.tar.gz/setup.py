#!/usr/bin/env python
#-*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
        name = "ccsdk",
        version = "0.0.1",
        keywords = ("pip", "datacanvas", "eds", "jmhuang"),
        description = "cc sdk",
        long_description = "cc sdk for python",
        license = "MIT License",

        url = "http://jmhuang.me",
        author = "jmhuang",
        author_email = "jmhuang@corp.netease.com",

        packages = find_packages(),
        include_package_data = True,
        platforms = "any",
        install_requires = []
)
