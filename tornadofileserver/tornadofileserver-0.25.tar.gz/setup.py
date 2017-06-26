# -*- coding: utf-8 -*-
# sudo python setup.py register sdist upload

from distutils.core import setup

PACKAGE = "tornadofileserver"
NAME = "tornadofileserver"
DESCRIPTION = "tornado simple HttpService."
AUTHOR = "syf"
AUTHOR_EMAIL = "git@suyafei.com"
URL = "https://github.com/myyyy"
VERSION = '0.25'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    # long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache License, Version 2.0",
    url=URL,
    packages=["tornadofileserver"],
    package_data={'tornadofileserver': ['static/*',
         'templates/index.html'
     ]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    zip_safe=False,
)
