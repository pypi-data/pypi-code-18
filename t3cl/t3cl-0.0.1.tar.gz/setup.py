#!coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import json
import codecs
import setuptools

setup = {}
version = {}

pwd = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(pwd, 'setup.json'), encoding = 'utf-8') as handle:
    setup.update(json.load(handle))

with codecs.open(os.path.join(pwd, 't3cl/__about__.py'), encoding = 'utf-8') as handle:
    exec(handle.read(), version)

with codecs.open(os.path.join(pwd, 'README.rst'), encoding = 'utf-8') as handle:
    long_description = handle.read()

setup['name'] = version['__title__']
setup['description'] = version['__summary__']
setup['url'] = version['__url__']
setup['version'] = version['__version__']
setup['author'] = version['__author__']
setup['author_email'] = version['__email__']
setup['license'] = version['__license__']
setup['long_description'] = long_description
setup['packages'] = setuptools.find_packages(exclude = ['contrib', 'docs', 'tests'])

setuptools.setup(**setup)
