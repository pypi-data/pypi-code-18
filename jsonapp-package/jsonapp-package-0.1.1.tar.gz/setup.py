#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'xerox==0.4.1',
    'six==1.10.0',
]

setup(
    name='jsonapp-package',
    version='0.1.1',
    description="A command line utility that helps dealing with JSON data.",
    long_description=readme + '\n\n' + history,
    author="Eyal Levin",
    author_email='eyalev@gmail.com',
    url='https://github.com/eyalev/jsonapp',
    packages=[
        'jsonapp',
    ],
    package_dir={'jsonapp':
                 'jsonapp'},
    entry_points={
        'console_scripts': [
            'jsonapp=jsonapp.jsonapp_cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='jsonapp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
)
