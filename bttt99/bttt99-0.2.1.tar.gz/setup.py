#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'lxml',
    'requests',
    'click',
    'pyperclip'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='bttt99',
    version='0.2.1',
    description="A tool to navigate movie information.",
    long_description=readme + '\n\n' + history,
    author="Stephen Chen",
    author_email='noemail@noemail.com',
    url='https://github.com/babykick/bttt99',
    packages=[
        'bttt99',
    ],
    package_dir={'bttt99':
                 'bttt99'},
    entry_points={
        'console_scripts': [
            'bttt99=bttt99.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='bttt99',
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
    tests_require=test_requirements
)
