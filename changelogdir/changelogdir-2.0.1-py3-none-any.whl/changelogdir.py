# -*- coding: utf-8 -*-
#
# Copyright (C) 2017  Carmen Bianca Bakker <carmen@carmenbianca.eu>
#
# This file is part of changelogdir.
#
# changelogdir is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# changelogdir is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with changelogdir.  If not, see <http://www.gnu.org/licenses/>.

"""Generate changelogs from a directory structure to avoid merge conflicts."""

import argparse
import configparser
import pathlib
import sys
from os import path

__author__ = 'Carmen Bianca Bakker <carmen@carmenbianca.eu>'
__all__ = []
__version__ = '2.0.1'

# pylint: disable=too-few-public-methods,missing-docstring,redefined-outer-name


class Path:

    def __init__(self, path):
        self.path = pathlib.Path(path)

    def __lt__(self, other):
        return self.path < other.path

    def __repr__(self):
        return repr(self.path)

class Tree(Path):

    def __init__(self, path):
        super().__init__(path)
        self.sections = []


class Section(Path):

    def __init__(self, path):
        super().__init__(path)
        self.subsections = []
        self.entries = []


class Subsection(Path):

    def __init__(self, path):
        super().__init__(path)
        self.entries = []


class Entry(Path):

    def __init__(self, path):
        super().__init__(path)


def filter_name(name):
    """The gist of this function: Turn '001_hello' into 'hello'.

    Basically, remove the stuff before the first underscore, including the
    underscore itself.
    """
    if '_' in name:
        return name.split('_', 1)[1]
    return name


def default_config():
    """Generate a default config object.

    :return: Configuration.
    :rtype: :class:`ConfigParser`
    """
    defaults = {
        'directory': 'CHANGELOG',
        'file_extension': 'md',
        'header': '# Changelog',
        'section_header': '## {section_name}',
        'subsection_header': '### {subsection_name}',
    }
    config = configparser.ConfigParser()
    config.read_dict({'changelogdir': defaults})
    return config


def parse_config(config, config_file):
    """Parse *config_file*.

    :param config_file: File containing configuration.
    :type config_file: File-like object
    :return: Contents of parsed file.
    :rtype: :class:`ConfigParser`
    :raise: :class:`configparser.Error`
    """
    config.read_file(config_file)
    return config


def changelog_tree(directory, file_extension):
    """Create a tree from *directory*.

    Root level is *directory*.

    The first level contains all the version sections.

    The second level contains either subsection directories, or entry files.
    Some of the entry files may be special files such as 'date' that describe
    the version section in more detail.

    The third level contains entry files.

    :param str directory: Changelog directory.
    :param str file_extension: Extension of entry files.
    :return: A tree of all changelog sections, subsections, and entries.
    :rtype: :class:`Tree`
    """
    if not file_extension.startswith('.'):
        file_extension = '.' + file_extension
    tree = Tree(directory)
    if not tree.path.is_dir():
        raise ValueError('{} is not a directory'.format(repr(directory)))
    tree.sections = list(reversed(sorted(Section(section)
                                         for section in tree.path.iterdir()
                                         if section.is_dir())))
    for section in tree.sections:
        section.subsections = sorted(Subsection(sub)
                                     for sub in section.path.iterdir()
                                     if sub.is_dir())
        section.entries = sorted(Entry(entry)
                                 for entry in section.path.iterdir()
                                 if entry.is_file()
                                 and entry.suffix == file_extension)
        for sub in section.subsections:
            sub.entries = sorted(Entry(entry) for entry in sub.path.iterdir()
                                 if entry.is_file()
                                 and entry.suffix == file_extension)

    return tree


def render_section(section, write_func, config):
    """Write *section* with *write_func*.

    :param section: A changelog section.
    :type section: :class:`Section` or :class:`Subsection`.
    :param write_func: A write function.
    :type write_func: Function
    :param config: Configuration.
    :type config: :class:`ConfigParser`
    """
    name = filter_name(section.path.name)
    # First, render our header
    if isinstance(section, Section):
        date_file = section.path / 'date'
        if date_file.exists():
            with date_file.open() as fp:
                date = fp.read().strip('\n')
        else:
            date = ''
        write_func(config['section_header'].format(
            section_name=name, section_date=date))
    else:
        write_func(config['subsection_header'].format(
            subsection_name=name))

    write_func('\n')

    for entry in section.entries:
        write_func('\n')
        with entry.path.open() as fp:
            contents = fp.read()
        write_func(contents)

    subsections = getattr(section, 'subsections', None)
    if subsections:
        for subsection in subsections:
            write_func('\n')
            render_section(subsection, write_func, config)


def render(tree, write_func, config):
    """Write *tree* with *write_func*."""
    write_func(config['header'])
    write_func('\n')

    for section in tree.sections:
        write_func('\n')
        render_section(section, write_func, config)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description='Generate changelogs from a directory structure.',
        epilog='If no output file is specified, write to STDOUT.')
    parser.add_argument('-o', '--output', help='File to write to')
    parser.add_argument('-c', '--config',
                        help="Path to config file (default: '.changelogdirrc')")
    parser.add_argument('-d', '--directory',
                        help='Override path to changelog directory')
    parsed = parser.parse_args(argv)

    config = default_config()
    config_path = (parsed.config if parsed.config is not None
                   else '.changelogdirrc')
    fp = None

    try:
        fp = open(config_path)
    except IOError as e:
        # If config was specified but does not exist, raise an error.  If it
        # was not specified, then that's no problem; we'll just use the
        # defaults.
        if parsed.config is not None:
            raise configparser.Error(
                '{} is not a valid configuration file'.format(
                    repr(parsed.config))) from e

    # Read config file if one was found.
    if fp is not None:
        try:
            config = parse_config(config, fp)
        except configparser.Error as e:
            raise configparser.Error(
                '{} is not a valid configuration file'.format(
                    repr(parsed.config))) from e
        finally:
            fp.close()

    config = config['changelogdir']

    directory = (parsed.directory
                 if parsed.directory else
                 path.join(path.dirname(config_path), config['directory']))
    tree = changelog_tree(directory, config['file_extension'])

    # If output file was specified, write to that file.  Else, write to STDOUT.
    if parsed.output:
        with open(parsed.output, 'w') as output_file:
            render(tree, output_file.write, config)
    else:
        render(tree, sys.stdout.write, config)


if __name__ == '__main__':
    main()
