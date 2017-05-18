"""The main script of redis-naming-py."""

DELIMITER = ':'


class NoKeyFieldsError(Exception):
    """The error should be raised when any key fileds is not specified."""

    pass


class NoValueFieldsError(Exception):
    """The error should be raised when any value fields is not specified."""

    pass


class TooManyFieldsError(Exception):
    """The error should be raised when the field values are too many."""

    pass


class TooLessFieldsError(Exception):
    """The error should be raised when the field values are too less."""

    pass


class UnexpectedFieldError(Exception):
    """The error should be raised when the unexpected field value exists."""

    def __init__(self, unexpected_field):
        """Set the unexpected field as the error cause."""
        super(UnexpectedFieldError, self).__init__()
        self.unexpected_field = unexpected_field


class RedisNamer(object):
    """Manage the field settings of key and value."""

    def __init__(self, key_field=None, key_fields=None, value_field=None,
                 value_fields=None):
        """Set the field settings of key and value."""
        self.key_fields = key_fields
        if self.key_fields is None:
            self.key_fields = [] if key_field is None else [key_field]
        if len(self.key_fields) == 0:
            raise NoKeyFieldsError()

        self.value_fields = value_fields
        if self.value_fields is None:
            self.value_fields = [] if value_field is None else [value_field]
        if len(self.value_fields) == 0:
            raise NoValueFieldsError()

    def name_key(self, *args, **kwargs):
        """Build the key name."""
        key = ''
        if len(args) > 0:
            if len(args) > len(self.key_fields):
                raise TooManyFieldsError()
            elif len(args) < len(self.key_fields):
                raise TooLessFieldsError()
            for key_field, arg in zip(self.key_fields, args):
                if key != '':
                    key += DELIMITER
                key += key_field
                key += DELIMITER
                key += arg
        else:
            for arg in kwargs.keys():
                if arg not in self.key_fields:
                    raise UnexpectedFieldError(unexpected_field=arg)
            for key_field in self.key_fields:
                if key != '':
                    key += DELIMITER
                key += key_field
                key += DELIMITER
                key += kwargs[key_field]

        # If value field is only one, concatenate the value field name to tail
        if len(self.value_fields) == 1:
            key += DELIMITER
            key += self.value_fields[0]
        return key

    def name_value(self, *args, **kwargs):
        """Build the value name."""
        # TODO: support args param

        if len(args) > 0:
            if len(args) > len(self.value_fields):
                raise TooManyFieldsError()
            elif len(args) < len(self.value_fields):
                raise TooLessFieldsError()

            # If value field is only one, return value only because value field
            # name should be concatenated to key
            if len(self.value_fields) == 1:
                return args[0]

            value = ''
            for arg, value_field in zip(args, self.value_fields):
                if value != '':
                    value += DELIMITER
                value += value_field
                value += DELIMITER
                value += arg
            return value
        else:
            for arg in kwargs.keys():
                if arg not in self.value_fields:
                    raise UnexpectedFieldError(unexpected_field=arg)

            # If value field is only one, return value only because value field
            # name should be concatenated to key
            if len(self.value_fields) == 1:
                value_field = self.value_fields[0]
                return kwargs[value_field]

            value = ''
            for value_field in self.value_fields:
                if value != '':
                    value += DELIMITER
                value += value_field
                value += DELIMITER
                value += kwargs[value_field]
            return value
