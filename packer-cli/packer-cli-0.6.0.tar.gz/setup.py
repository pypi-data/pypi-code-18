#!/usr/bin/env python

"""
Packer install script
"""

import pathlib
import re
from setuptools import find_packages, setup

def read_requirements(filename):
    """
    Reads requirements from the given file
    """

    with open(filename) as file_handle:
        return file_handle.readlines()

with open('README.rst') as readme_file:
    README = readme_file.read()

with open(pathlib.Path('src', 'packer', '__init__.py'), 'r') as init_file:
    VERSION = re.search(
        r'^__version__\s*=\s*[\'\"](?P<version>[^\'\"]+)[\'\"]$',
        init_file.read(),
        re.MULTILINE,
    ).group('version')

REQUIREMENTS = read_requirements(pathlib.Path('requirements', 'release.txt'))
TEST_REQUIREMENTS = read_requirements(pathlib.Path('requirements', 'test.txt'))

setup(
    name='packer-cli',
    version=VERSION,
    description='Command line utility for converting data to different formats',
    long_description=README,
    author='James Durand',
    author_email='james.durand@alumni.msoe.edu',
    url='https://github.com/durandj/packer',
    license='MIT license',
    packages=find_packages(where='src'),
    package_dir={
        '': 'src',
    },
    include_package_data=True,
    install_requires=REQUIREMENTS,
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False,
    keywords='packer',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'packer=packer.cli:packer_cli',
        ],
    },
)
