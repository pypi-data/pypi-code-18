"""Setuptools entry point."""

import os
import codecs
from setuptools import setup, find_packages

from kinesisutils import __version__, __author__

dirname = os.path.dirname(__file__)
description = "Kinesis utilities"

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, RuntimeError):
    if os.path.isfile("README.md"):
        long_description = codecs.open(os.path.join(dirname, "README.md"),
                                       encoding="utf-8").read()
    else:
        long_description = description

setup(
    name="kinesisutils",
    include_package_data=True,
    package_data={
        "": ["*.j2", "*.yaml"]},
    packages=find_packages(include=["kinesisutils"]),
    version=__version__,
    author=__author__,
    author_email="german@findhotel.net",
    url="https://github.com/findhotel/kinesisutils",
    license="MIT",
    description=description,
    long_description=long_description,
    install_requires=[
        "boto3",
        "retrying",
        "wrapt",
        ],
    classifiers=[
        "Programming Language :: Python :: 3"]
)
