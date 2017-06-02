#!/usr/bin/env python
from __future__ import with_statement

import sys
try:
    from setuptools import setup 
except ImportError:
    from distutils.core import setup

IS_PYPY = hasattr(sys, 'pypy_translation_info')
DESCRIPTION = "hjs, the missing bit of hjson-py"

with open('README.rst', 'r') as f:
   LONG_DESCRIPTION = f.read()

CLASSIFIERS = filter(None, map(str.strip,
"""
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: MIT License
License :: OSI Approved :: Academic Free License (AFL)
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Topic :: Software Development :: Libraries :: Python Modules
""".splitlines()))

if __name__ == "__main__":
    setup(
        name="hjs",
        use_scm_version=True,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        keywords="json comments configuration",
        classifiers=CLASSIFIERS,
        author="Charbel Jacquin",
        author_email="charbel.jacquin@gmail.com",
        url="http://github.com/charbeljc/hjs",
        license="MIT License",
        packages=['hjs', 'hjs.tests'],
        platforms=['any'],
        install_requires=['hjson', 'six'],
        setup_requires=['setuptools_scm'])

