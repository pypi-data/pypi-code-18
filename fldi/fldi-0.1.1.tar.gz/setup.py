# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""
print('xxxxxxxxxxxxx')
print(find_packages())
setup(
    name="fldi",
    version="0.1.1",
    description="A dependency injection container",
    license="MIT",
    author="Ádám Gólya",
    packages=find_packages(),
    install_requires=['dotmap'],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ]
)
