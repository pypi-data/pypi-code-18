#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
        name='fcfuzz',
        version='0.2.3',
        description='python3 based computer security suite',
        author ='nullp0inter',
        author_email ='nicetry@fbi.gov',
        license  = 'None',
        keywords = 'nullp0nter fcfuzz',
        packages = find_packages(exclude=['resources']),
    )
