#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# Author: locke
# Mail: lockeCucumber@163.com
# Created Time:  2017-06-21 19:16:16
#############################################

from setuptools import setup, find_packages

setup(
    name = "pyxdiamond",
    version = "1.0.0",
    keywords = ("pip", "datacanvas", "xdiamond", "lockeCucumber"),
    description = "xdiamond sdk",
    long_description = "xdiamond sdk for python",
    license = "MIT Licence",

    author = "lockeCucumber",
    author_email = "lockeCucumber@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests"]
)
