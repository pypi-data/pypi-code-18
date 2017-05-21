# -*- coding: utf-8 -*-

"""The setup.py file for Save Your Time SSH."""

from setuptools import setup, find_packages
from pip.req import parse_requirements

REQUIREMENTS = parse_requirements('requirements.txt', session='hack')
INSTALL_REQUIRES = [str(ir.req) for ir in REQUIREMENTS]


with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

setup(
    name='sytssh',
    version='0.0.1',
    description='A ssh helper to save your time',
    long_description=README,
    author='Felipe Alexandre Rodrigues',
    author_email='felipear89@gmail.com',
    url='https://github.com/felipear89/pyssh',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs')),
    scripts=['bin/sytssh'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=INSTALL_REQUIRES
)
