# encoding=UTF-8

# Copyright © 2013-2017 Jakub Wilk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

import tools

def get_mod_paths():
    stdlib_dir = os.path.dirname(os.__file__)
    for root, dirs, files in os.walk(stdlib_dir):
        for path in files:
            for d in ['site-packages', 'dist-packages']:
                try:
                    dirs.remove(d)
                except ValueError:
                    pass
            if path.endswith('.py'):
                path = os.path.join(root, path)
                yield path

def test():
    paths = list(get_mod_paths())
    tools.run_pydiatra(paths, expected=None, parallel=True)

# vim:ts=4 sts=4 sw=4 et
