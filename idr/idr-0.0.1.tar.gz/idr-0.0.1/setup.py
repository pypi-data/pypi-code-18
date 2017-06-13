#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# Hack to prevent stupid "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when running `python
# setup.py test` or `python setup.py flake8`.  See:
#  * http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
#  * https://github.com/getsentry/raven-python/blob/master/setup.py
import multiprocessing
assert multiprocessing  # silence flake8

VERSION = '0.0.1'


def get_requirements(suffix=''):
    with open('requirements%s.txt' % suffix) as f:
        rv = f.read().splitlines()
    return rv


class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def read(fname):
    """
    Utility function to read the README file.
    :rtype : String
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='idr',
    version=VERSION,
    description='Image Data Repository access library',
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 '
        'or later (GPLv2+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],  # Get strings from
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='The Open Microscopy Team',
    author_email='ome-devel@lists.openmicroscopy.org.uk',
    url='https://github.com/idr/idr-python',
    license='GPLv2+',
    packages=find_packages(),
    zip_safe=True,
    include_package_data=True,
    platforms='any',
    setup_requires=['flake8'],
    install_requires=get_requirements(),
    tests_require=get_requirements('-dev'),
    entry_points="""
    # -*- Entry points: -*-
    """,
    cmdclass={'test': PyTest},
)
