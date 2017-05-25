from suitcase.structure import Structure
from c2log.fields import FixedLengthString
from c2log.fields import UBInt16Sequence


class FLStruct(Structure):
    string = FixedLengthString(6)


def test_unpack_fixed_length_string():
    string = b'asdf\x00\x00'
    data = FLStruct.from_data(string)

    assert len(data.string) == 4
    assert data.string == b'asdf'


def test_pack_fixed_length_string():
    string = FLStruct()
    string.string = b'\x61\x73\x64\x66\x00\x00'

    packed = string.pack()
    assert packed == b'asdf'


class UBInt16Seq(Structure):
    ubint16seq = UBInt16Sequence(2)


def test_ubint16_sequence():
    seq = UBInt16Seq()
    seq.ubint16seq = (0, 1)

    assert seq.pack() == b'\x00\x00\x00\x01'

    seq = UBInt16Seq.from_data(b'\x00\x00\x00\x01')
    assert seq.ubint16seq == (0, 1)
