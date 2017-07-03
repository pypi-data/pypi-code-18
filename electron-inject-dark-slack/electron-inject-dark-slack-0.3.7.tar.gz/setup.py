#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except Exception:
        return "Not available"
setup(
    name="electron-inject-dark-slack",
    version="0.3.7",
    packages=["electron_inject_dark_slack"],
    author="KemonoServal",
    author_email="wrdqex@gmail.com",
    description=(
        "A fork of electron-inject to inject a dark css theme into the slack desktop app"),
    license="GPLv3",
    keywords=["electron", "inject", "slack", "dark theme"],
    url="https://github.com/KemonoServal/electron-inject-dark-slack",
    download_url="https://github.com/KemonoServal/electron-inject-dark-slack/tarball/v0.3",
    #python setup.py register -r https://testpypi.python.org/pypi
    long_description=read("README.rst") if os.path.isfile("README.rst") else read("README.md"),
    install_requires=['websocket-client','requests'],
	package_dir={'electron_inject_dark_slack': 'electron_inject_dark_slack'},
    package_data={
                  'electron_inject_dark_slack': ['electron_inject_dark_slack']
                  },
	include_package_data=True
)
