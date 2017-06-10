#!/usr/bin/env python

from setuptools import setup, find_packages
from restricted_pkg import setup

config = {
    'private_repository': 'http://@upload.localhost',
    'name' : 'atodorov-test',
    'version' : '0.4',
    'packages' : find_packages(),
    'author' : 'Alexander Todorov',
    'author_email' : 'atodorov@nopam.otb.bg',
    'license' : 'BSD',
    "description" : 'Dummy test package, please ignore.',
    'long_description' : 'Test package',
    'url' : 'https://github.com/atodorov/bztest',
}

setup(**config)
