# configstack/__init__.py
# Part of ConfigStack, a library for configuring Python programs.
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

"""
ConfigStack: a library for configuring Python programs.

ConfigStack is a Python library for stacking program configuration:

* Command-line options, defined with `argparse`.

* Environment variables, derived from other configuration options.

* Configuration files, defined with `configparser`.

* Default values.

These are all unified at run time, in a single collection of settings
for the program to use.
"""

from .layers import *
from .sources import *
from .structures import *


# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied. See the file ‘LICENSE.GPL-3’ for details.


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
