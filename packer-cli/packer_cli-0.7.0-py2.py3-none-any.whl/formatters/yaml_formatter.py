"""
YAML specific formatter implementation
"""

import typing

import yaml.parser

import packer.errors
from .base import Formatter

class YAMLFormatter(Formatter):
    """
    YAML specific formatter implementation
    """

    format_name = 'yaml'

    # pylint: disable=bad-whitespace
    def __init__(self, data_stream: typing.IO[typing.Any], indent: int=4) -> None:
    # pylint: disable=bad-whitespace
        super().__init__(data_stream)

        self.indent = indent

    def format_pretty(self) -> str:
        return self._format(indent=self.indent, default_flow_style=False)

    def format_compact(self) -> str:
        return self._format()

    def parse(self, data_stream: typing.IO[typing.Any]) -> typing.Any:
        try:
            return yaml.load(data_stream)
        except yaml.parser.ParserError as ex:
            raise packer.errors.PackerMalformedDataError(ex)

    def _format(self, **kwargs) -> str:
        return yaml.dump(self.data, **kwargs)
