#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages
import sqlinclause

setup(
    name             = 'sqlinclause',
    version          = sqlinclause.__version__,
    description      = 'SQL utility to write variable length IN-clause.',
    license          = sqlinclause.__license__,
    author           = sqlinclause.__author__,
    author_email     = 'takuma-miura@m3.com',
    url              = '',
    keywords         = 'SQL IN',
    packages         = ['sqlinclause'],
    install_requires = ['sqlparse'],
)

