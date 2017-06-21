#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# Author: locke
# Mail: wentaohuang@epiclouds.net
# Created Time:  2017-06-01 19:16:16
#############################################

from setuptools import setup, find_packages

setup(
    name = "xdiamond_jiayun",
    version = "1.0.1",
    keywords = ("pip", "datacanvas", "xdiamond_jiayun", "lockeCucumber"),
    description = "xdiamond_jiayun sdk",
    long_description = "xdiamond_jiayun sdk for python",
    license = "MIT Licence",

    author = "lockeCucumber",
    author_email = "lockeCucumber@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests"]
)
