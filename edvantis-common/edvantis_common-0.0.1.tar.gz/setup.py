import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="edvantis_common",
    version="0.0.1",
    author="Mykhailo Malkush",
    author_email="mm.malkush@gmail.com",
    description="",
    license="BSD",
    keywords="edvantis",
    url="http://packages.python.org/edvantis_common",
    packages=['common'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
