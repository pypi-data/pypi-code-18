
from datetime import datetime


class StringBaseUtil(object):

    def __init__(self, string):
        self.string = string

    def to_datetime(self):

        _datetime = None

        formats = [
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d',
        ]

        exceptions = []

        for _format in formats:

            try:
                _datetime = datetime.strptime(self.string, _format)
                return _datetime

            except ValueError as e:
                exceptions.append(e)

        if _datetime is None:
            raise exceptions[-1]
