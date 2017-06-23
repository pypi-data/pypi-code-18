from enum import IntFlag
from inspect import isclass

from motorengine.fields import BaseField


def as_int(value):
    """
    Coerce a value to an integer, interpreting strings as binary.

    This function can raise a TypeError if `value` is not a string or integer,
    or a ValueError if it cannot be interpreted as an integer.

    Examples:
    >>> as_int('10010100')
    148
    >>> as_int(b'0b10010100')
    148
    >>> as_int(148)
    148
    >>> as_int([1, 2, 3])
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: int() argument must be a string, a bytes-like object or a number, not 'list'
    >>> as_int('not a binary string')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: invalid literal for int() with base 2: 'not a binary string'
    """
    # int has a nasty api where passing a base for non-strings raises a TypeError
    # >>> int(1, 10)
    # Traceback (most recent call last):
    #   File "<string>", line 1, in <module>
    # TypeError: int() can't convert non-string with explicit base
    string_types = (bytes, bytearray, str)

    if isinstance(value, string_types):
        i = int(value, base=2)
    else:
        i = int(value)

    return i


class BitField(BaseField):
    """
    A field for storing packed bits that deserialize to `enum.IntFlag` types.

    Examples:
    >>> # create some flags to use in our example
    >>> class UserFlags(IntFlag):
    ...     IS_ACTIVE                = auto()
    ...     IS_ADMIN                 = auto()
    ...     HAS_LOGGED_IN            = auto()
    ...     HAS_SEEN_INTRO           = auto()
    ...     SUBSCRIBED_TO_NEWSLETTER = auto()
    ...
    >>> # use the flags in our Document mapping
    >>> class User(Document):
    ...     name = StringField()
    ...     email = StringField()
    ...     flags = BitField(UserFlags)
    ...
    >>> # flags are serialized into an integer
    >>> id = loop.run_until_complete(
    ...     User.objects.create(
    ...         name='Bit Field',
    ...         email='example@bitfield.py',
    ...         flags=(UserFlags.IS_ACTIVE | UserFlags.SUBSCRIBED_TO_NEWSLETTER)
    ...     )
    ... )
    >>> # and deserialized into the original enum
    >>> user = loop.run_until_complete(
    ...     User.objects.get(id)
    ... )
    >>> user.flags
    <UserFlags.IS_ACTIVE|SUBSCRIBED_TO_NEWSLETTER: 17>
    >>> bool(user.flags & UserFlags.IS_ADMIN)
    False
    >>> # User can also be created with integers or strings of binary
    >>> User.flags.from_son(2**5 - 1)
    <UserFlags.IS_ACTIVE|IS_ADMIN|HAS_LOGGED_IN|HAS_SEEN_INTRO|SUBSCRIBED_TO_NEWSLETTER: 31>
    >>> as_son = User.flags.to_son('01101')
    >>> User.flags.from_son(as_son)
    <UserFlags.IS_ACTIVE|HAS_LOGGED_IN|HAS_SEEN_INTRO: 21>
    """

    def __init__(self, enum_type, *, max_bits=None, **kwargs):
        """
        Create a new BitField object.

        This function can raise a TypeError if the `enum_type` is not a
        subclass of `enum.IntFlag`.
        """

        if not isclass(enum_type) or not issubclass(enum_type, IntFlag):
            raise TypeError(f'{enum_type!r} is not an enum.')

        self.enum_type = enum_type
        self.max_bits = max_bits

        super().__init__(**kwargs)


    def to_son(self, value):
        if value is None:
            return None

        return as_int(value)


    def from_son(self, value):
        if value is None:
            return None

        return self.enum_type(value)


    def validate(self, value):
        if value is None:
            return True

        try:
            i = as_int(value)
        except (TypeError, ValueError):
            return False

        return i.bit_length() > self.max_bits if self.max_bits else True
