#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   This file is part of the Murdock project.
#
#   Copyright 2016 Malte Lichtner
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Module `murdocktools.options`
-----------------------------

Collect and print all configuration (file) options currently implemented in
Murdock. The documentation for the command-line tool is found :ref:`here <Configuration Option Collector>`.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys

import murdock
from murdock.runner.runner import get_config_options


def fmt_murdock_options(mode, descriptions=False, required=False, rst=False):
    """Return a formatted tree of Murdock configuration options.

    Args:
        mode (str): Murdock mode, i.e. `docking`, `screening` or `training`.
        descriptions (bool): Add the option descriptions.
        required (bool): Include only required options without a default value.
        rst (bool): Format output in ReStructuredText format.

    Returns:
        str: The formatted configuration option tree.

    """
    s = ''
    if rst:
        s += '%s\n%s\n' % (mode.capitalize(), len(mode) * '-')
    s += '%s' % _fmt_option_tree(
        mode, descriptions=descriptions, required=required, rst=rst)
    return s


def main():
    if _run():
        sys.exit(0)
    else:
        sys.exit(1)


def _fmt_option_tree(
        section, module=None, indent='', descriptions=False, required=False,
        rst=False):
    s = ''
    module, options = get_config_options(section, module)
    if not options:
        return s
    if not s.endswith('\n\n'):
        s += '\n'
    for opt in options:
        if required and (not opt.required or opt.default is not None):
            continue
        s += indent
        if opt.default is not None:
            tag = 'default: %s' % str(opt.default)
        elif opt.required:
            tag = 'required'
        else:
            tag = 'optional'
        if rst:
            s += '- ``%s`` `~%s.ConfigDeclaration.%s`' % (
                _fmt_type(opt.dtype), module.__name__[7:], opt.name)
            if not required:
                s += ' *(%s)*' % tag
        else:
            s += '[%s] "%s"' % (_fmt_type(opt.dtype), opt.name)
            if not required:
                s += ' (%s)' % tag
        if descriptions:
            s += ': %s' % opt.description
        if not s.endswith('\n\n'):
            s += '\n'
        s += _fmt_option_tree(
            opt.name, module, indent + '  ', descriptions=descriptions,
            required=required, rst=rst)
    if not s.endswith('\n\n'):
        s += '\n'
    return s


def _parse_command_line():
    """Parse, validate and return command line arguments.
    """
    cmdline_parser = argparse.ArgumentParser(
        description='Murdock v%s configuration option index' %
        murdock.__version__)
    cmdline_parser.add_argument(
        'mode', type=str, choices=['docking', 'screening', 'training'],
        help='Murdock mode')
    cmdline_parser.add_argument(
        '--no-descriptions', action='store_true', help='do not print '
        'configuration option descriptions')
    cmdline_parser.add_argument(
        '--rest', action='store_true', help='print in ReStructuredTest (ReST) '
        'format')
    cmdline_parser.add_argument(
        '-r', '--required-only', action='store_true', help='do not print '
        'optional configuration options')
    cmdline = cmdline_parser.parse_args()
    return cmdline


def _fmt_type(dtype):
    comparators = {'lt': '<', 'le': '<=', 'gt': '>', 'ge': '>='}
    special = {'zero': '0'}
    try:
        t, c, s = dtype.__name__.split('_')
        return '%s %s %s' % (t, comparators[c], special[s])
    except (AttributeError, KeyError, ValueError):
        return dtype.__name__


def _run():
    cmdline = _parse_command_line()
    descriptions = not cmdline.no_descriptions
    print(fmt_murdock_options(
        cmdline.mode, descriptions=descriptions,
        required=cmdline.required_only, rst=cmdline.rest))
    return True


if __name__ == '__main__':
    main()


