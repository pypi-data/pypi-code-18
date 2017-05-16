#!/usr/bin/env python
from distutils.core import setup
from os.path import abspath, dirname, join
from redtube import __version__

here = abspath(dirname(__file__))

setup(
    name='python3-redtube',
    version=__version__,
    license="BSD",
    description="module to access RedTube API - updated to Python 3",
    long_description="".join(open(join(here, 'README.rst')).readlines()),
    author="Don Ramon / sthrnbeau",
    author_email="sthrnbeau94@gmail.com",
    url="https://bitbucket.org/sthrnbeau/python3-redtube",
    py_modules=["redtube"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.6",
        "License :: OSI Approved :: BSD License",
        "Environment :: Web Environment",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Education",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Multimedia :: Video"
    ],
    keywords="redtube api client adult"
)
