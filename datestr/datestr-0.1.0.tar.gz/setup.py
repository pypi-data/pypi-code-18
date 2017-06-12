#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'future',
    'python-dateutil',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='datestr',
    version='0.1.0',
    description="Wrapper object around relativedelta to manage date and datetime strings",
    long_description=readme,
    author="Mohamed Cherkaoui",
    author_email='chermed@gmail.com',
    url='https://github.com/chermed/datestr',
    packages=[
        'datestr',
    ],
    package_dir={'datestr':
                 'datestr'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='datestr date datetime odoo string convert',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
