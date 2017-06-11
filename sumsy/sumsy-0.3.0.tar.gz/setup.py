#!/usr/bin/env python
#-*- coding: utf-8 -*-

from setuptools import find_packages, setup


with open('requirements.txt') as requirements_file:
    requirements = [ requirement[:-1] for requirement in requirements_file ]

setup(
    name='sumsy',
    description='A forklift who greatly resembles another forklift',
    version='0.3.0',
    author='João Abecasis',
    author_email='joao@abecasis.name',
    url='https://github.com/biochimia/sumsy',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'sumsy = sumsy.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',
    ],
)
