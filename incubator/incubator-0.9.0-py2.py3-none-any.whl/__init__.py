"""
<!---
The MIT License (MIT)

Copyright (c) 2017 Frantisek Lachman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->
[![build status](https://gitlab.com/lachmanfrantisek/incubator/badges/master/build.svg)
](https://gitlab.com/lachmanfrantisek/incubator/commits/master)
[![coverage report](https://gitlab.com/lachmanfrantisek/incubator/badges/master/coverage.svg)
](https://gitlab.com/lachmanfrantisek/incubator/commits/master)
[![License: MIT](https://img.shields.io/pypi/l/incubator.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/documentation-pdoc-green.svg)](https://lachmanfrantisek.gitlab.io/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/v/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/status/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/pyversions/incubator.svg)](https://pypi.python.org/pypi/incubator/)

---------

**Incubator is a Python API and command line interface for building container images in better and more secure way.**

With Incubator you can:

* precisely control layering of the image
* mounting build-time volumes (for secrets present only during the build)
* better metadata handling
* use standard *Dockerfile* (extended functionality is defined externally)

Source is hosted at [gitlab.com/lachmanfrantisek/incubator](https://gitlab.com/lachmanfrantisek/incubator).
"""

import logging

import os
import pkg_resources
import incubator.core.constants as _const

try:
    __version__ = pkg_resources.require(_const.APP_NAME)[0].version
except:
    _dirname = os.path.dirname(os.path.abspath(__file__))
    _version_file = open(os.path.join(_dirname, os.pardir, 'VERSION'))
    __version__ = _version_file.read().strip()


def set_logging(name=_const.APP_NAME, level=logging.DEBUG, handler=None, add_handler=True):
    """
    Set logging handler for the logger.

    * name: (str) name of the logger
    * level: logging level
    * handler: logging handler to add to logger
    * add_handler: (bool) whether to add handler to logger
    """
    logger = logging.getLogger(name)
    logger.handlers = []
    logger.setLevel(level)

    if add_handler:
        if not handler:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)

        logger.addHandler(handler)
