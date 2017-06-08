# configstack/layers.py
# Part of ConfigStack, a library for configuring Python programs.
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Stacks of program configuration. """

from . import sources
from . import structures
from .exceptions import LayerNotPopulatedError


__all__ = [
        'LayerNotPopulatedError',
        'ConfigLayer',
        'DefaultConfigLayer',
        'EnvironmentConfigLayer',
        'ConfigparserConfigLayer',
        'ConfigStack',
        ]


class ConfigLayer:
    """ A layer of configuration for reading. """

    #: Class to use for creating a default source for this layer.
    configsource_class = type(NotImplemented)

    def __init__(self, name, source=None):
        self.name = name

        if source is None:
            source = self.make_default_source()
        self.source = source

    def make_default_source(self):
        """ Make an instance of this layer's default ConfigSource class. """
        source = self.configsource_class()
        return source

    def __repr__(self):
        text = "<{type} {name} source: {source}>".format(
                type=type(self).__name__,
                name=self.name,
                source=repr(self.source),
                )
        return text

    def __str__(self):
        text = "{type} {name} source: {source}".format(
                type=type(self).__name__,
                name=self.name,
                source=str(self.source),
                )
        return text

    class NotPopulatedError(LayerNotPopulatedError):
        pass

    def populate(self):
        """ Populate this layer from its source. """
        self._sections = self.source.sections()

    def sections(self):
        """ Get the collection of configuration sections. """
        if not hasattr(self, '_sections'):
            raise self.NotPopulatedError(
                    "layer {!r} is not yet populated".format(self))

        return self._sections


class DefaultConfigLayer(ConfigLayer):
    """ A layer of configuration holding the option defaults. """

    default_name = "DEFAULT"
    configsource_class = sources.DefaultConfigSource

    def __init__(self, name=default_name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)


class EnvironmentConfigLayer(ConfigLayer):
    """ A layer of configuration from environment variables. """

    default_name = "ENVIRONMENT"
    configsource_class = sources.EnvironmentConfigSource

    def __init__(self, name=default_name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)


class ConfigparserConfigLayer(ConfigLayer):
    """ A layer of configuration from configuration files. """

    default_name = "CONFIGPARSER"
    configsource_class = sources.ConfigParserConfigSource

    def __init__(self, name=default_name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)


class ConfigStack:
    """ A stack of configuration layers. """

    def __init__(self, layers, *args, **kwargs):
        self.layers = layers
        super().__init__(*args, **kwargs)

    def __repr__(self):
        text = "<{type} layers: {layers!r}>".format(
                type=type(self).__name__,
                layers=self.layers,
                )
        return text

    def __str__(self):
        text = "{type} layers: [{layers}]".format(
                type=type(self).__name__,
                layers=", ".join(layer.name for layer in self.layers),
                )
        return text

    def sections(self):
        """ Get the aggregate collection of sections for this stack. """
        sections = {}
        for layer in self.layers:
            for (section_name, layer_section) in layer.sections().items():
                section = sections.get(
                        section_name,
                        structures.ConfigSection(name=section_name))
                for (option_name, option_value) in layer_section.items():
                    if option_name not in section:
                        section[option_name] = option_value
                sections[section.name] = section

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
