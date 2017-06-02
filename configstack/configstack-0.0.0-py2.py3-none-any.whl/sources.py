# configstack/sources.py
# Part of ConfigStack, a library for configuring Python programs.
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Sources for configuration options. """

import abc
import configparser
import os
import re

from .structures import ConfigSection


__all__ = [
        'ConfigSource',
        'DefaultConfigSource',
        'EnvironmentConfigSource',
        'ConfigparserConfigSource',
        ]


class ConfigSource(metaclass=abc.ABCMeta):
    """ A source of configuration option values. """

    @abc.abstractmethod
    def sections(self):
        """ Get the sections available in this source. """


class DefaultConfigSource(ConfigSource):
    """ A source for program configuration defaults. """

    def __init__(self, sections):
        self._sections = sections

    def sections(self):
        return self._sections

    @classmethod
    def from_dict(cls, sections):
        """
        Make a `DefaultConfigSource` from the specified `sections` mapping.

        :param sections: A mapping {`name`: `options`} where `options`
            is a mapping of options for the section `name`.
        :return: A new `DefaultConfigSource` containing the
            `ConfigSection` instances derived from the specified
            `sections` mapping.
        """
        sections = {
                name: ConfigSection(name=name, options=options)
                for (name, options) in sections.items()}
        return cls(sections=sections)


class EnvironmentConfigSource(ConfigSource):
    """ A configuration source reading the process environment. """

    def __init__(self, program_name, *args, **kwargs):
        self.program_name = program_name

        self.variable_name_pattern = re.compile(
                """
                ^
                # The program name.
                {program}_
                # The section name.
                (?P<section>[A-Z0-9]+)_
                # The option name.
                (?P<option>[A-Z0-9_]+)
                $
                """.format(program=self.program_name.upper()),
                re.VERBOSE)

        super().__init__(*args, **kwargs)

    def sections(self):
        """ Get the sections determined by the environment variables. """
        candidate_variables = {
                name: value
                for (name, value) in os.environ.items()
                if self.variable_name_pattern.match(name)}

        sections = {}
        for (name, value) in candidate_variables.items():
            match = self.variable_name_pattern.match(name)
            section_name_upper = match.group('section')
            section_name = section_name_upper.lower()
            if section_name not in sections:
                sections[section_name] = ConfigSection(name=section_name)
            section = sections[section_name]

            option_name_upper = match.group('option')
            option_name = option_name_upper.lower()
            section[option_name] = value

        return sections


class ConfigparserConfigSource(ConfigSource):
    """ A configuration source reading configuration files. """

    def __init__(self, filenames, *args, **kwargs):
        self.filenames = filenames
        self.parser = configparser.ConfigParser()

        super().__init__(*args, **kwargs)

    def sections(self):
        self.parser.read(filenames=self.filenames)
        sections = {name: None for name in self.parser.sections()}
        for section_name in sections.keys():
            options = {}
            for option_name in self.parser.options(section_name):
                options[option_name] = self.parser.get(
                        section_name, option_name)
            sections[section_name] = ConfigSection(
                    name=section_name,
                    options=options,
                    )
        return sections


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
