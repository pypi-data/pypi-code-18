#
# setup.py
#
# Copyright (c) 2016-2017 Junpei Kawamoto
#
# This file is part of rgmining-dataset-io.
#
# rgmining-dataset-io is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-dataset-io is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rgmining-dataset-io. If not, see <http://www.gnu.org/licenses/>.
#
"""Package information of dataset I/O library for review graph mining project.
"""
from os import path
from setuptools import setup, find_packages


def read(fname):
    """Read a file.
    """
    return open(path.join(path.dirname(__file__), fname)).read()


def load_requires_from_file(filepath):
    """Read a package list from a given file path.

    Args:
      filepath: file path of the package list.

    Returns:
      a list of package names.
    """
    with open(filepath) as fp:  # pylint: disable=invalid-name
        return [pkg_name.strip() for pkg_name in fp.readlines()]


setup(
    name='rgmining-dataset-io',
    use_scm_version=True,
    author="Junpei Kawamoto",
    author_email="kawamoto.junpei@gmail.com",
    description="Dataset I/O for Review graph mining project",
    long_description=read("README.rst"),
    url="https://github.com/rgmining/common",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    setup_requires=[
        "setuptools_scm"
    ],
    install_requires=load_requires_from_file("requirements.txt"),
    test_suite='tests.suite',
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ]
)
