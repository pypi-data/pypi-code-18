#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='grill-names',
    version='0.0.1',
    packages=find_packages(exclude=("*.tests", "*.tests.*", "tests.*", "tests", "*.docs", "*.docs.*", "docs.*", "docs")),
    description='Name objects for digital content creation.',
    author='Christian Lopez Barron',
    author_email='chris.gfz@gmail.com',
    url='https://github.com/thegrill/grill-names',
    download_url='https://github.com/thegrill/grill-names/releases/tag/0.0.1',
    classifiers=['Programming Language :: Python :: 3.6'],
    extras_require={'docs': ['sphinx_autodoc_typehints']},
    install_requires=['naming'],
    namespace_packages=['grill']
)
