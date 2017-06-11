#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup

setup(
    name            = 'django-staticfiles-downloader',
    version         = '0.1.0',
    description     = 'Django staticfiles extension to download third-party static files',
    author          = 'Jakub Dorňák',
    author_email    = 'jakub.dornak@misli.cz',
    license         = 'BSD',
    url             = 'https://github.com/misli/django-staticfiles-downloader',
    packages        = ['staticfiles_downloader'],
    classifiers     = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)
