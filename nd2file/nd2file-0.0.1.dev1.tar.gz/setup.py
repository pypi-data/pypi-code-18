# -*- coding: utf-8 -*-
"""
documentation
"""

from setuptools import setup, find_packages

setup(
    name='nd2file',
    version='0.0.1.dev1',
    description='Access Nikon NIS-Elements ND2 files',
    long_description='see https://github.com/csachs/nd2file',
    author='Christian C. Sachs',
    author_email='sachs.christian@gmail.com',
    url='https://github.com/csachs/nd2file',
    packages=find_packages(),
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'
    ]
)
