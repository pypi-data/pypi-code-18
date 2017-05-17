# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)

# Copyright 2016 Chris Kirkos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup
from os.path import join as pathjoin, dirname

def read(*rnames):
    return open(pathjoin(dirname(__file__), *rnames)).read()

setup(
    name = 'txtelegraf',
    version = '0.2.1',
    author = "Christopher Kirkos",
    author_email = "offero@gmail.com",
    url = "https://github.com/offero/txtelegraf",
    download_url = 'https://github.com/offero/txtelegraf/archive/v0.2.1.zip',
    license="Apache License 2.0",
    description = "A TCP/UDP Telegraf/InfluxDB client for Twisted.",
    long_description = read('README.rst'),
    packages = [str('txtelegraf')],
    install_requires = ['twisted'],
    keywords=["twisted", "telegraf", "influxdb"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
