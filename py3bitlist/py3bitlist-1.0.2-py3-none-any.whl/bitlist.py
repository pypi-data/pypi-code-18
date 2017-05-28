class BitList:
    
    def __init__(self, length):
        if not type(length) is int:
            raise TypeError
        self.bytes_length = length // 8 + 1
        self.length = self.bytes_length * 8
        self.main_object = bytearray(self.bytes_length)

    def get_bytes_length(self):
        return self.bytes_length

    def get_length(self):
        return self.length

    def set_bit(self, position, num):
        if not type(position) is int:
            raise TypeError
        byte_pos = position // 8
        bit_pos = position % 8
        target_byte = self.main_object[byte_pos]
        if num == 0:
            self.main_object[byte_pos] = target_byte & (~(1 << bit_pos))
        else:
            self.main_object[byte_pos] = target_byte | (1 << bit_pos)
        
    def get_bit(self, position):
        if not type(position) is int:
            raise TypeError
        byte_pos = position // 8
        bit_pos = position % 8
        target_byte = self.main_object[byte_pos]
        return (target_byte >> bit_pos) & 1
