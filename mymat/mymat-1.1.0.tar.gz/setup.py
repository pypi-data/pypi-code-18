# -*- coding: utf-8 -*-

import codecs
import os
# import sys

#try:
from setuptools import setup
#except:
#    from distutils.core import setup


def read(fname):
    """
    define read method to read the long description.
    It will be shown in PyPI，
"""
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "mymat"

PACKAGES = ["mymat",]

DESCRIPTION = "Subclass of numpy.matrix behaving as matrices in matlab."

LONG_DESCRIPTION = read("README.txt")

KEYWORDS = "numpy matrix matlab"

AUTHOR = "William Song"

AUTHOR_EMAIL = "songcwzjut@163.com"

URL = "https://git.oschina.net/williamzjc/mymat"

VERSION = "1.1.0"

LICENSE = "MIT"


setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: Public Domain',  # Public Domain
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Natural Language :: English'
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)