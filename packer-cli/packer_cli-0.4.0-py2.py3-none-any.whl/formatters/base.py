"""
Base formatter implementation
"""

import abc
import typing

import packer.errors

class Formatter(metaclass=abc.ABCMeta):
    """
    Base formatter implementation
    """

    formatters: typing.ClassVar[typing.Dict[str, typing.Type]] = {}

    def __init_subclass__(cls):
        """
        Register any subclasses as possible formatters
        """

        if not hasattr(cls, 'format_name'):
            raise packer.errors.PackerError(
                f'{cls} is missing the format_name attribute',
            )

        format_name = getattr(cls, 'format_name')
        Formatter.formatters[format_name] = cls

    def __init__(self, data_stream: typing.IO[typing.Any]) -> None:
        """
        Creates a formatter loaded with the given data in a parsed form
        """

        self.data = self.parse(data_stream)

    @abc.abstractmethod
    def format_pretty(self) -> str:
        """
        Formats the data in a human friendly form
        """

    @abc.abstractmethod
    def format_compact(self) -> str:
        """
        Formats the data in a compact form
        """

    @abc.abstractmethod
    def parse(self, data_stream: typing.IO[typing.Any]) -> typing.Any:
        """
        Parses the data stream and returns the parsed data
        """

    @classmethod
    def get_formatter_class(cls, format_name: str) -> typing.Type:
        """
        Gets a class for the given format type
        """

        if format_name not in cls.formatters:
            raise packer.errors.PackerUnknownFormatType(
                f'Unrecognized format type: {format_name}',
            )

        return cls.formatters[format_name]
