"""
JSON specific formatter
"""

import json
import typing

import packer.errors
from .base import Formatter

class JSONFormatter(Formatter):
    """
    JSON specific formatter implementation
    """

    format_name = 'json'

    # pylint: disable=bad-whitespace
    def __init__(self, data_stream: typing.IO[typing.Any], indent: int=4) -> None:
    # pylint: enable=bad-whitespace
        super().__init__(data_stream)

        self.indent = indent

    def format_pretty(self) -> str:
        return self._format(indent=self.indent)

    def format_compact(self) -> str:
        return self._format()

    def parse(self, data_stream: typing.IO[typing.Any]) -> typing.Any:
        try:
            return json.load(data_stream)
        except json.JSONDecodeError as ex:
            raise packer.errors.PackerMalformedDataError(ex)

    def _format(self, **kwargs):
        return json.dumps(self.data, **kwargs)
