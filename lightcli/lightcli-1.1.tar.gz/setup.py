#!/usr/bin/env python3

#_MIT License
#_
#_Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)
#_
#_Permission is hereby granted, free of charge, to any person obtaining a copy
#_of this software and associated documentation files (the "Software"), to deal
#_in the Software without restriction, including without limitation the rights
#_to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#_copies of the Software, and to permit persons to whom the Software is
#_furnished to do so, subject to the following conditions:
#_
#_The above copyright notice and this permission notice shall be included in all
#_copies or substantial portions of the Software.
#_
#_THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#_IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#_FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#_AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#_LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#_OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#_SOFTWARE.

"""
Lightcli
--------

Lightcli is a Python 3 library module for lightweight terminal interaction.

Synopsis
````````

::

    import lightcli
    
    choice = lightcli.choice_input([options=<options>], [prompt=<prompt>], [showopts={True|False}], [qopt={True|False}])
    multiline = lightcli.long_input([prompt=<prompt>], [maxlines=<maxlines>], [maxlength=<maxlength>])
    mylist = lightcli.list_input([prompt=<prompt>], [maxitems=<maxitems>], [maxlength=<maxlength>])
    outputfile = lightcli.outfile_input([extension=<extension>])


Links
`````

* `Documentation <https://github.com/dogoncouch/lightcli/blob/master/README.md>`_
* `Releases <https://github.com/dogoncouch/lightcli/releases/>`_
* `Changelog <https://github.com/dogoncouch/lightcli/blob/master/CHANGELOG.md>`_
"""

from setuptools import setup
from os.path import join
from sys import prefix
from lightcli import __version__

ourdata = [(join(prefix, 'share/man/man3'), ['doc/lightcli.3']),
        (join(prefix, 'share/doc/lightcli'), ['README.md', 'LICENSE'])]

setup(name = 'lightcli', version = str(__version__),
        description = 'A lightweight terminal interaction library for Python',
        long_description = __doc__,
        author = 'Dan Persons', author_email = 'dpersonsdev@gmail.com',
        url = 'https://github.com/dogoncouch/lightcli',
        keywords = ['python-library', 'python3-library', 'input',
            'input-method', 'python-module', 'python3-module', 'cli',
            'cli-utilities', 'input-validation'],
        py_modules = ['lightcli'],
        data_files = ourdata,
        classifiers = ["Development Status :: 5 - Production/Stable",
            "Environment :: Other Environment",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries :: Python Modules"])
