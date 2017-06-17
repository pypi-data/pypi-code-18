#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

long_description = readme

setup(
    name='python-c',
    version='v1.0',
    description='A lazy alternative to python -c',
    long_description=long_description,
    author='Jad Nohra',
    author_email='jadnohra@gmail.com',
    license='MIT',
    url='https://github.com/jadnohra/python-c',
    download_url = 'https://github.com/jadnohra/python-c/archive/v1.0.tar.gz',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'python-c = python_c.python_c:main',
        ]
    },
)
