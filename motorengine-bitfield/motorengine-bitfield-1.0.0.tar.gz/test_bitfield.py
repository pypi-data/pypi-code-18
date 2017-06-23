from enum import auto, IntFlag

from bitfield import BitField
import pytest


class UserFlags(IntFlag):
    a = auto()
    b = auto()
    c = auto()
    d = auto()


class TestBitField:

    def test_create_bit_field(self):
        field = BitField(UserFlags, max_bits=8)

        assert field.enum_type == UserFlags
        assert field.max_bits == 8


    def test_create_bit_field_error(self):
        with pytest.raises(TypeError):
            field = BitField(object())


    @pytest.mark.parametrize("value,as_son", [
        (UserFlags.a, int(UserFlags.a)),
        (5, 5),
        (0b0101, 5),
        ('0b0101', 5),
        ('0101', 5),
        (b'0b0101', 5),
        (b'0101', 5),
        (bytearray(b'0b0101'), 5),
        (bytearray(b'0101'), 5),
        (True, 1),
        (False, 0),
        (None, None),
    ])
    def test_to_son(self, value, as_son):
        field = BitField(UserFlags)

        assert field.to_son(value) == as_son


    @pytest.mark.parametrize("value,as_son", [
        (UserFlags.a, int(UserFlags.a)),
        (5, 5),
        (0b0101, 5),
        (True, 1),
        (False, 0),
        (None, None),
    ])
    def test_from_son(self, value, as_son):
        field = BitField(UserFlags)

        if value is None:
            assert field.from_son(value) is None
        else:
            assert field.from_son(as_son) == UserFlags(value)


    @pytest.mark.parametrize("value,is_valid", [
        (UserFlags.a, True),
        (5, True),
        (0b0101, True),
        ('0b0101', True),
        ('0101', True),
        (b'0b0101', True),
        (b'0101', True),
        (bytearray(b'0b0101'), True),
        (bytearray(b'0101'), True),
        (True, True),
        (False, True),
        (None, True),
        ('', False),
        ('abc', False),
        (b'', False),
        (b'abc', False),
        (bytearray(b''), False),
        (bytearray(b'abc'), False),
        (object(), False),
        (list(), False),
        (dict(), False),
        (type, False),
    ])
    def test_validate(self, value, is_valid):
        field = BitField(UserFlags)

        assert field.validate(value) == is_valid


    @pytest.mark.parametrize("value,is_valid", [
        (UserFlags.a, True),
        (UserFlags.c, False),
        (1, True),
        (5, False),
        (0b01, True),
        (0b0101, False),
        ('0b01', True),
        ('0b0101', False),
        ('01', True),
        ('0101', False),
        (b'0b01', True),
        (b'0b0101', False),
        (b'01', True),
        (b'0101', False),
        (bytearray(b'0b01'), True),
        (bytearray(b'0b0101'), False),
        (bytearray(b'01'), True),
        (bytearray(b'0101'), False),
        (True, True),
        (False, True),
        (None, True),
        ('', False),
        ('abc', False),
        (b'', False),
        (b'abc', False),
        (bytearray(b''), False),
        (bytearray(b'abc'), False),
        (object(), False),
        (list(), False),
        (dict(), False),
        (type, False),
    ])
    def test_validate_max_bits(self, value, is_valid):
        field = BitField(UserFlags, max_bits=2)
