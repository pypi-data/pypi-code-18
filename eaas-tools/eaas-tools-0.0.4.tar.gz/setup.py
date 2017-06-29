#!/usr/bin/python

from setuptools import setup

setup(
    name="eaas-tools",
    version="0.0.4",
    description="Client Tools for EAAS",
    author="Ian Norton",
    author_email="inorton@gmail.com",
    url="https://github.com/inorton/eaas",
    packages=["eaaslib"],
    scripts=["eaas", "eaas-list", "eaassh"],
    platforms=["any"],
    license="License :: OSI Approved :: MIT License",
    install_requires=["python-etcd"],
    long_description="Find and use EAAS instances")

