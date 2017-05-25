from suitcase.fields import BaseField
from suitcase.fields import BaseFixedByteSequence


class UBInt16Sequence(BaseFixedByteSequence):
    "A sequence of unsigned, big-endian 16 bit integers"

    def __init__(self, length, **kwargs):
        super().__init__(lambda l: ">" + "H" * l, length, **kwargs)
        self.bytes_required = length * 2


class FixedLengthString(BaseField):
    """
    Reads a fixed number of bytes (interpreted as ASCII) from input stream
    """

    def __init__(self, length, **kwargs):
        super().__init__(**kwargs)
        self.length = length

    @property
    def bytes_required(self):
        "Number of bytes to read from stream"
        return self.length

    def pack(self, stream):
        stream.write(self._value.strip(b'\0'))

    def unpack(self, data):
        self._value = data.strip(b'\0')
