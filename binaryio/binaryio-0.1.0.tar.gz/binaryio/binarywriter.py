import io
import struct


class BinaryWriter(io.BufferedWriter):
    def __init__(self, raw):
        super().__init__(raw)
        self.endianness = ""

    def align(self, alignment):
        super().seek(-super().tell() % alignment, io.SEEK_CUR)

    def seek(self, offset, whence=io.SEEK_SET):
        super().seek(offset, whence)

    def tell(self):
        return super().tell()

    def write_0_string(self, value, encoding="ascii"):
        self.write_raw_string(value, encoding)
        self.write_byte(0)

    def write_byte(self, value):
        super().write(struct.pack("B", value))

    def write_bytes(self, value):
        super().write(value)

    def write_int32(self, value):
        super().write(struct.pack(self.endianness + "i", value))

    def write_int32s(self, value):
        super().write(struct.pack(self.endianness + str(len(value)) + "i", *value))

    def write_sbyte(self, value):
        super().write(struct.pack(self.endianness + "b", value))

    def write_sbytes(self, value):
        super().write(struct.pack(self.endianness + str(len(value)) + "b", *value))

    def write_single(self, value):
        super().write(struct.pack(self.endianness + "f", value))

    def write_singles(self, value):
        super().write(struct.pack(self.endianness + str(len(value)) + "f", *value))

    def write_uint16(self, value):
        super().write(struct.pack(self.endianness + "H", value))

    def write_uint16s(self, value):
        super().write(struct.pack(self.endianness + str(len(value)) + "H", *value))

    def write_uint32(self, value):
        super().write(struct.pack(self.endianness + "I", value))

    def write_uint32s(self, value):
        super().write(struct.pack(self.endianness + str(len(value)) + "I", *value))

    def write_raw_string(self, value, encoding="ascii"):
        super().write(bytearray(value, encoding))
