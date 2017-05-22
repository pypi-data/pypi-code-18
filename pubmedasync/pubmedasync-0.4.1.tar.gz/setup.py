#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'aiodns>=1.1.1',
    'aiohttp>=1.2.0',
    'beautifulsoup4>=4.5.1',
    'cchardet>=1.1.1',
    'lxml>=3.7.0',
    'tqdm>=4.10.0',
]

test_requirements = [
]

setup(
    name='pubmedasync',
    version='0.4.1',
    description="Asyncronous wrapper around PubMed api",
    long_description=readme + '\n\n' + history,
    author="Pokey Rule",
    author_email='pokey.rule@gmail.com',
    url='https://github.com/pokey/pubmedasync',
    packages=[
        'pubmedasync',
    ],
    package_dir={'pubmedasync':
                 'pubmedasync'},
    entry_points={
        'console_scripts': [
            'pubmedasync=pubmedasync.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pubmedasync',
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
