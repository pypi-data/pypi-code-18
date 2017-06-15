#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

setup(
    name="Rumba",
    version="0.4",
    url="https://gitlab.com/arcfire/rumba",
    keywords="rina measurement testbed",
    author="Sander Vrijders",
    author_email="sander.vrijders@intec.ugent.be",
    license="LGPL",
    description="Rumba measurement framework for RINA",
    packages=["rumba", "rumba.testbeds", "rumba.prototypes"],
    install_requires=["paramiko", "wheel", "wget"],
    scripts = ['tools/rumba-access']
)
