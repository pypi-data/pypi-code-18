#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
        name="arsdkxml",
        version="0.9.1",
        packages=find_packages(),
        package_data={
                        'xml': ['arsdkxml/xml/*.xml'],
                        '': ['README.md']
                     },
        zip_safe=False,
        include_package_data=True,
        author="Ya-Liang Chang",
        author_email="allen314x@yahoo.com.tw",
        description="Unofficial python parser for Parrot drones xml",
        platforms="Linux",
        license="BSD",
        keywords="bebop python control xml",
        url="https://github.com/amjltc295/arsdkxml"
    )
