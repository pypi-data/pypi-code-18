#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='remove_emoji',
    version='0.0.1',
    description=(
        'remove emojis from string, as description, comment and etc.'
    ),
    author='fanjun',
    author_email='handsomefun@126.compile',
    maintainer='fanjun',
    maintainer_email='handsomefun@126.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["linux ucs2"],
    url='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
    ]
)
