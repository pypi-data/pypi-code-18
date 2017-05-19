import uuid
from datetime import datetime, timezone

from msgpack import ExtType
import pytest

from msgpack_ext import msgpack


test_data = [
    (
        b'\xd8\x01\xbf\x12\xf6#"\x14E\\\xa4\xdc\xdb\x84\xecK\x0c\x03',
        uuid.UUID('bf12f623-2214-455c-a4dc-db84ec4b0c03')
    ),
    (
        b'\xd7\x02A\xdf\xff\xff\xff\xc0\x00\x00',
        datetime(2038, 1, 19, 3, 14, 7, tzinfo=timezone.utc)
    ),
    (
        b'\x81\xa7__exc__\x94\xa8builtins\xaaValueError\x92\xa3foo\xa3bar\xc0',
        ValueError('foo', 'bar')
    )
]


@pytest.mark.parametrize("msg,native", test_data)
def test_encode(msg, native):
    assert msgpack.packb(native) == msg


@pytest.mark.parametrize("msg,native", test_data)
def test_decode(msg, native):
    if isinstance(native, BaseException):
        unpacked = msgpack.unpackb(msg)
        assert isinstance(unpacked, type(native))
        assert unpacked.args == native.args
    else:
        assert msgpack.unpackb(msg) == native


def test_encode_fallback():
    class C:
        pass

    with pytest.raises(TypeError):
        msgpack.packb(C)


def test_decode_fallback():
    assert msgpack.unpackb(b'\xc7\x00*') == ExtType(42, b'')
