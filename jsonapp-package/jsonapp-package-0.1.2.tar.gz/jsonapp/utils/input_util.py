from datetime import datetime

from collections import OrderedDict

import six

from jsonapp.utils.string_base_util import StringBaseUtil


def validate_datetime_string(datetime_string):
    StringBaseUtil(datetime_string).to_datetime()


class Input(object):

    def __init__(self, _input):
        self.input = _input

    def to_datetime(self):

        if self.is_string():
            return StringBaseUtil(self.input).to_datetime()

        if self.is_datetime():
            return self.input

        if self.is_float():
            return datetime.utcfromtimestamp(self.input)

    def to_date(self):
        return datetime.strptime(self.input, '%Y-%m-%d').date()

    def to_datetime_string(self):

        if self.is_datetime():
            return self.input.isoformat()

        if self.is_string():
            return self.input

        if self.is_float():
            return self.to_datetime().isoformat()

    def to_datetime_milliseconds_string(self):

        datetime_string = self.to_datetime_string()

        if len(datetime_string) == 26:
            return datetime_string[0:-3]

        else:
            return datetime_string

    def is_string(self):
        return isinstance(self.input, six.string_types)

    def is_datetime(self):

        return isinstance(self.input, datetime)

    def is_float(self):

        return isinstance(self.input, float)

    def is_odict(self):

        return isinstance(self.input, OrderedDict)

    def is_list(self):

        return isinstance(self.input, list)

    def is_int(self):

        return isinstance(self.input, int)

    def is_valid_datetime_string(self):

        try:
            if self.input:
                _datetime = StringBaseUtil(self.input).to_datetime()

                if _datetime and isinstance(_datetime, datetime):
                    return True

            return False

        except ValueError:
            return False

    def is_not_valid_datetime_string(self):

        return not self.is_valid_datetime_string()
