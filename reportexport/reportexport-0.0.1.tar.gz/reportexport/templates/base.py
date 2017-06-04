# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod, abstractproperty

from ..exceptions import InvalidTemplate, AlreadyRegisteredError


class Template:
    """Template that renders a report."""

    __metaclass__ = ABCMeta

    _TEMPLATES = {}

    @classmethod
    @abstractproperty
    def extension(cls):
        """String to define the file extension correspondent to the template."""

    @staticmethod
    @abstractmethod
    def render(report):
        """Render a report instance into a buffer."""

    @classmethod
    def register(cls, template):
        """Add the template into the list of templates.

        Args:
            template(Template): template class to register
        """
        if template.extension in cls._TEMPLATES:
            raise AlreadyRegisteredError('Template for "{}" already registered.'.format(template.extension))

        cls._TEMPLATES[template.extension] = template

    @classmethod
    def deregister(cls, extension):
        del cls._TEMPLATES[extension]

    @classmethod
    def get_template(cls, extension):
        """Get the template for the given extension.

        Args:
            extension(str): extension of the file desired.

        Returns:
            (Template) class of the template that handles the extension desired
        """
        try:
            return cls._TEMPLATES[extension]
        except KeyError:
            raise InvalidTemplate

