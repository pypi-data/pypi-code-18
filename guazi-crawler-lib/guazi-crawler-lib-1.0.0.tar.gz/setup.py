#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='guazi-crawler-lib',
    version='1.0.0',
    description=(
        '瓜子爬虫公共库'
    ),
    long_description=open('README.md').read(),
    author='chendansi',
    author_email='chendansi@guazi.com',
    maintainer='chendansi',
    maintainer_email='chendansi@guazi.com',
    license='MIT',
    packages=find_packages(),
    platforms=["all"],
    install_requires=[],
    url='http://www.baidu.com',
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)