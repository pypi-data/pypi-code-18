# Copyright 2017 SrMouraSilva
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

from os import path
from setuptools import setup


def readme():
    here = path.abspath(path.dirname(__file__))

    with open(path.join(here, 'README.rst'), encoding='UTF-8') as f:
        return f.read()

setup(
    name='PedalPi-WebService',
    version='0.2.0',

    description='WebService (REST and WebSocket) to access and controller your Pedal Pi pedals set configurations',
    long_description=readme(),

    url='https://github.com/PedalPi/WebService',

    author='Paulo Mateus Moura da Silva (SrMouraSilva)',
    author_email='mateus.moura@hotmail.com',
    maintainer='Paulo Mateus Moura da Silva (SrMouraSilva)',
    maintainer_email='mateus.moura@hotmail.com',

    license="Apache Software License v2",

    packages=[
        'webservice',
        'webservice/handler',
        'webservice/search',
        'webservice/util',
        'webservice/websocket',
    ],

    package_data={},

    install_requires=[
        'PedalPi-Application',
        'tornado>=4.4.2',
        'tornado-cors==0.6.0',
        'zeroconf'
    ],

    test_suite='wstest',
    tests_requires=[
        'PedalPi-Application',
        'requests==2.11.1'
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Multimedia :: Sound/Audio',
        'Programming Language :: Python :: 3'
    ],
    keywords='pedal-pi mod-host lv2 audio plugins-manager pedal-pi-component',

    platforms='Linux',
)
