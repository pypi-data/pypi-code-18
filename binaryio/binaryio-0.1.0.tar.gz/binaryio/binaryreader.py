import io
import struct


class BinaryReader(io.BufferedReader):
    def __init__(self, raw):
        super().__init__(raw)
        self.endianness = ""

    def align(self, alignment):
        super().seek(-self.tell() % alignment, io.SEEK_CUR)

    def seek(self, offset, whence=io.SEEK_SET):
        super().seek(offset, whence)

    def tell(self):
        return super().tell()

    def read_0_string(self):
        text = ""
        i = self.read_byte()
        while i != 0:
            text += chr(i)
            i = self.read_byte()
        return text

    def read_byte(self):
        return super().read(1)[0]

    def read_bytes(self, count):
        return super().read(count)

    def read_int32(self):
        return struct.unpack(self.endianness + "i", super().read(4))[0]

    def read_int32s(self, count):
        return struct.unpack(self.endianness + str(int(count)) + "i", super().read(4 * count))

    def read_sbyte(self):
        return struct.unpack(self.endianness + "b", super().read(1))[0]

    def read_sbytes(self, count):
        return struct.unpack(self.endianness + str(int(count)) + "b", super().read(1 * count))

    def read_single(self):
        return struct.unpack(self.endianness + "f", super().read(4))[0]

    def read_singles(self, count):
        return struct.unpack(self.endianness + str(int(count)) + "f", super().read(4 * count))

    def read_uint16(self):
        return struct.unpack(self.endianness + "H", super().read(2))[0]

    def read_uint16s(self, count):
        return struct.unpack(self.endianness + str(int(count)) + "H", super().read(2 * count))

    def read_uint32(self):
        return struct.unpack(self.endianness + "I", super().read(4))[0]

    def read_uint32s(self, count):
        return struct.unpack(self.endianness + str(int(count)) + "I", super().read(4 * count))

    def read_raw_string(self, length, encoding="ascii"):
        return super().read(length).decode(encoding)
