#!/usr/bin/env python3
from os.path import dirname, realpath
from setuptools import find_packages, setup

with open('pymj/version.py') as source_file:
    exec(source_file.read())

def _read_requirements_file():
    req_file_path = '%s/requirements.txt' % dirname(realpath(__file__))
    with open(req_file_path) as f:
        return [line.strip() for line in f]


setup(
    name='pymj',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=_read_requirements_file())
