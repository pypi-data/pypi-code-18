#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "1.1"

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


setup(
    name="django-session-log",
    version=version,
    description="Logs django sessions. ",
    license="MIT",
    author="Visgean Skeloru",
    author_email="visgean@gmail.com",
    url="https://github.com/Visgean/django-session-log",
    packages=[
        "session_log",
    ],
    include_package_data=True,
    install_requires=[
        "django>=1.1.0",
        "django-appconf>=0.6",
        "python-dateutil"
    ],
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
