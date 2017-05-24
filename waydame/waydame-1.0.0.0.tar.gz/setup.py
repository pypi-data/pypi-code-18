#!/usr/lib/env python
# -*- encoding:utf-8 -*-

from setuptools import setup, find_packages


if __name__ == "__main__":
    setup(
        name = "waydame",
        version = "1.0.0.0",
        zip_safe = False,
        packages = find_packages(),

        author = "waydame",
        author_email = "waydame@gmail.com",
        description = "waydame's python library",
        long_description = "waydame's python library",

        url = "http://waydame.me/",
        license = "GPL",
        platforms = "any",
        keywords = [ "waydame" ],
        install_requires = [ "tornado" ],
    )
