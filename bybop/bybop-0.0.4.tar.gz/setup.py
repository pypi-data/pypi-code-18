#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
        name="bybop",
        version="0.0.4",
        packages=find_packages('src'),
        package_dir={'': 'src'},
        package_data={
                        'arsdk-xml': ['arsdk-xml/xml/*.xml']
                     },
        zip_safe=False,
        include_package_data=True,
        author="Ya-Liang Chang",
        author_email="allen314x@yahoo.com.tw",
        description="Bebop Drone control for python",
        platforms="Linux",
        license="BSD",
        keywords="bebop python control",
        url="https://github.com/amjltc295/bybop"
    )
