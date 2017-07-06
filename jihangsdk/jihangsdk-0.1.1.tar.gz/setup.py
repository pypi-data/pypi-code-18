#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: bangguo
# Mail: willyxq@gmail.com
# Created Time:  2017-07-05 10:26:34 PM
#############################################

from setuptools import setup, find_packages

setup(
    name = "jihangsdk",
    version = "0.1.1",
    keywords = ("pip", "datacanvas", "jihang", "bangguo"),
    description = "jihang sdk",
    long_description = "jihang sdk for python",
    license = "MIT Licence",
                            
    url = "http://xiaoh.me",
    author = "bangguo",
    author_email = "willyxq@gmail.com",

    packages = find_packages(),
    include_package_data = True,                           
    platforms = "any",
    install_requires = []
    )

