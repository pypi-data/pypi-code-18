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

    def format_pretty(self) -> str:
        return self._format(indent=4)

    def format_compact(self) -> str:
        return self._format()

    def parse(self, data_stream: typing.IO[typing.Any]) -> typing.Any:
        try:
            return json.load(data_stream)
        except json.JSONDecodeError as ex:
            raise packer.errors.PackerMalformedDataError(ex)

    def _format(self, **kwargs):
        return json.dumps(self.data, **kwargs)
