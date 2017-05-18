#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages
from rszio import version

setup(
    name='django-rszio',
    author='Chad Shryock',
    author_email='chad@keystone.works',
    description='Django wrapper for RSZ.IO',
    license='MIT',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/g3rd/django-rszio',
    zip_safe=True,
    install_requires=[
        'django>=1.10',
        'requests>=2.14.2',
    ],
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='django resize image',
)
