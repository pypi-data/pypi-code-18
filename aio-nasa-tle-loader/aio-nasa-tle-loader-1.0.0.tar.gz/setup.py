# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import re
import sys

import os
from setuptools import setup


if sys.version_info < (3, 5, 0):
    raise RuntimeError("aio-space-track-api requires Python 3.5.0+")


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_REGEXP = re.compile(r"^__version__ = [\'\"](.+?)[\'\"]$", re.MULTILINE)


def read(fn):
    with codecs.open(os.path.join(PROJECT_DIR, fn), encoding='utf-8') as f:
        return f.read().strip()


def version():
    try:
        return VERSION_REGEXP.findall(read(os.path.join('aio_nasa_tle_loader', '__init__.py')))[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


vn = version()
url = 'https://github.com/nkoshell/aio-nasa-tle-loader'

setup(
    name='aio-nasa-tle-loader',
    description='Small async wrapper for `nasa-tle-loader` package',
    long_description=read('README.rst'),
    version=vn,
    packages=['aio_nasa_tle_loader'],
    url=url,
    download_url='{url}/archive/{version}.tar.gz'.format(url=url, version=vn),
    license='MIT',
    author='nkoshell',
    author_email='nikita.koshelev@gmail.com',
    install_requires=['aiohttp>=2.0.7', 'nasa-tle-loader>=1.0.0'],
)
