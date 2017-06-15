#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The Datakortet Basic utilities package: `dk`.
"""

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.3
Topic :: Software Development :: Libraries
"""

import sys
import setuptools
from setuptools import setup, Command
from setuptools.command.test import test as TestCommand

version = '0.7.9'


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='dk',
    version=version,
    requires=[],
    install_requires=[
        'six',
        'ipaddr',  # from dk.iplist
    ],
    description=__doc__.strip(),
    classifiers=[line for line in classifiers.split('\n') if line],
    long_description=open('README.rst').read(),
    license="LGPL",
    author='Bjorn Pettersen',
    author_email='bp@datakortet.no',
    url="http://www.github.com/datakortet/dk/",
    download_url='https://www.github.com/datakortet/dk',
    cmdclass={'test': PyTest},
    packages=setuptools.find_packages(exclude=['tests*']),
    zip_safe=False,
)
