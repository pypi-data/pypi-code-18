#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='simright-csrf',
    version='0.0.5',
    description=(
        'www.simright.com csrf token'
    ),
    author='<yangjiaronga>',
    author_email='yangjiaronga@gmail.com',
    maintainer='<yangjiaronga>',
    maintainer_email='<yangjiaronga@gmail.com>',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'Flask>=0.12',
        'itsdangerous>=0.24',
        'Werkzeug>=0.11.11'
    ]
)