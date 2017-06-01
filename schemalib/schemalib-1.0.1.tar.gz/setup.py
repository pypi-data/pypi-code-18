#!/usr/bin/python
from setuptools import setup, find_packages

def get_requirements():
    with open('requirements.txt') as fd:
        return fd.read().splitlines()

setup(
    name='schemalib',
    version='1.0.1',
    packages=find_packages(),
    install_requires=get_requirements(),
    include_package_data=True,
    author='Pavel Odvody',
    author_email='podvody@redhat.com',
    description='Library for working with JSON Schemas',
    long_description=open('README.md').read(),
    license='GPLv-3',
    keywords='lib',
    url='https://github.com/shaded-enmity/schemalib'
)
