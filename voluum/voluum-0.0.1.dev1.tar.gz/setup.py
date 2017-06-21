import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="voluum",
    version="0.0.1.dev1",
    author="Mateusz Sikora",
    author_email="sikora2048@gmail.com",
    description=("Python client for Voluum API"),
    license="BSD",
    keywords="python voluum api client",
    url="https://github.com/mateusz-sikora/python-voluum",
    packages=find_packages(),
    long_description='',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console'
    ],
)
