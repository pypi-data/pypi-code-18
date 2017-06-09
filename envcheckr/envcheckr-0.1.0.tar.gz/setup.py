#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='envcheckr',
    version='0.1.0',
    description="A really simple CLI tool to check and compare two .env files for missing variables",
    long_description=readme,
    author="Adam Goldin",
    author_email='adamjace@gmail.com',
    url='https://github.com/adamjace/envcheckr',
    download_url = 'https://github.com/adamjace/envcheckr/archive/0.1.tar.gz',
    packages=[
        'envcheckr',
    ],
    package_dir={'envcheckr':
                 'envcheckr'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords=['envcheckr', 'cli', 'env', 'environment', 'variables'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
