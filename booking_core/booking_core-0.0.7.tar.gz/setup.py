#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='booking_core',
    version='0.0.7',
    description='Booking engine API',
    author='Jonathan Rodriguez Alejos',
    author_email='jrodriguez.5716@gmail.com',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    url='https://gitlab.com/booking-4geeks/booking-core',
    download_url="https://gitlab.com/booking-4geeks/booking-core/repository/archive.tar.gz?ref=v0.7",
    packages=find_packages(),
    tests_require=[
        'future'
    ]
)
