'''
File Record Read/Write Messages
-------------------------------

Currently none of these messages are implemented
'''
import struct
from pymodbus.pdu import ModbusRequest
from pymodbus.pdu import ModbusResponse
from pymodbus.pdu import ModbusExceptions as merror
from pymodbus.compat import byte2int


#---------------------------------------------------------------------------#
# File Record Types
#---------------------------------------------------------------------------#
class FileRecord(object):
    ''' Represents a file record and its relevant data.
    '''

    def __init__(self, **kwargs):
        ''' Initializes a new instance

        :params reference_type: Defaults to 0x06 (must be)
        :params file_number: Indicates which file number we are reading
        :params record_number: Indicates which record in the file
        :params record_data: The actual data of the record
        :params record_length: The length in registers of the record
        :params response_length: The length in bytes of the record
        '''
        self.reference_type  = kwargs.get('reference_type', 0x06)
        self.file_number     = kwargs.get('file_number', 0x00)
        self.record_number   = kwargs.get('record_number', 0x00)
        self.record_data     = kwargs.get('record_data', '')

        self.record_length   = kwargs.get('record_length',   len(self.record_data) // 2)
        self.response_length = kwargs.get('response_length', len(self.record_data) + 1)

    def __eq__(self, relf):
        ''' Compares the left object to the right
        '''
        return self.reference_type == relf.reference_type \
           and self.file_number    == relf.file_number    \
           and self.record_number  == relf.record_number  \
           and self.record_length  == relf.record_length  \
           and self.record_data    == relf.record_data

    def __ne__(self, relf):
        ''' Compares the left object to the right
        '''
        return not self.__eq__(relf)

    def __repr__(self):
        ''' Gives a representation of the file record
        '''
        params = (self.file_number, self.record_number, self.record_length)
        return 'FileRecord(file=%d, record=%d, length=%d)' % params


#---------------------------------------------------------------------------#
# File Requests/Responses
#---------------------------------------------------------------------------#
class ReadFileRecordRequest(ModbusRequest):
    '''
    This function code is used to perform a file record read. All request
    data lengths are provided in terms of number of bytes and all record
    lengths are provided in terms of registers.

    A file is an organization of records. Each file contains 10000 records,
    addressed 0000 to 9999 decimal or 0x0000 to 0x270f. For example, record
    12 is addressed as 12. The function can read multiple groups of
    references. The groups can be separating (non-contiguous), but the
    references within each group must be sequential. Each group is defined
    in a seperate 'sub-request' field that contains seven bytes::

        The reference type: 1 byte (must be 0x06)
        The file number: 2 bytes
        The starting record number within the file: 2 bytes
        The length of the record to be read: 2 bytes

    The quantity of registers to be read, combined with all other fields
    in the expected response, must not exceed the allowable length of the
    MODBUS PDU: 235 bytes.
    '''
    function_code = 0x14
    _rtu_byte_count_pos = 2

    def __init__(self, records=None, **kwargs):
        ''' Initializes a new instance

        :param records: The file record requests to be read
        '''
        ModbusRequest.__init__(self, **kwargs)
        self.records  = records or []

    def encode(self):
        ''' Encodes the request packet

        :returns: The byte encoded packet
        '''
        packet = struct.pack('B', len(self.records) * 7)
        for record in self.records:
            packet += struct.pack('>BHHH', 0x06, record.file_number,
                record.record_number, record.record_length)
        return packet

    def decode(self, data):
        ''' Decodes the incoming request

        :param data: The data to decode into the address
        '''
        self.records = []
        byte_count = byte2int(data[0])
        for count in range(1, byte_count, 7):
            decoded = struct.unpack('>BHHH', data[count:count+7])
            record  = FileRecord(file_number=decoded[1],
                record_number=decoded[2], record_length=decoded[3])
            if decoded[0] == 0x06: self.records.append(record)

    def execute(self, context):
        ''' Run a read exeception status request against the store

        :param context: The datastore to request from
        :returns: The populated response
        '''
        # TODO do some new context operation here
        # if file number, record number, or address + length
        # is too big, return an error.
        files = []
        return ReadFileRecordResponse(files)


class ReadFileRecordResponse(ModbusResponse):
    '''
    The normal response is a series of 'sub-responses,' one for each
    'sub-request.' The byte count field is the total combined count of
    bytes in all 'sub-responses.' In addition, each 'sub-response'
    contains a field that shows its own byte count.
    '''
    function_code = 0x14
    _rtu_byte_count_pos = 2

    def __init__(self, records=None, **kwargs):
        ''' Initializes a new instance

        :param records: The requested file records
        '''
        ModbusResponse.__init__(self, **kwargs)
        self.records = records or []

    def encode(self):
        ''' Encodes the response

        :returns: The byte encoded message
        '''
        total  = sum(record.response_length + 1 for record in self.records)
        packet = struct.pack('B', total)
        for record in self.records:
            packet += struct.pack('>BB', 0x06, record.record_length)
            packet += record.record_data
        return packet

    def decode(self, data):
        ''' Decodes a the response

        :param data: The packet data to decode
        '''
        count, self.records = 1, []
        byte_count = byte2int(data[0])
        while count < byte_count:
            response_length, reference_type = struct.unpack('>BB', data[count:count+2])
            count += response_length + 1 # the count is not included
            record = FileRecord(response_length=response_length,
                record_data=data[count - response_length + 1:count])
            if reference_type == 0x06: self.records.append(record)


class WriteFileRecordRequest(ModbusRequest):
    '''
    This function code is used to perform a file record write. All
    request data lengths are provided in terms of number of bytes
    and all record lengths are provided in terms of the number of 16
    bit words.
    '''
    function_code = 0x15
    _rtu_byte_count_pos = 2

    def __init__(self, records=None, **kwargs):
        ''' Initializes a new instance

        :param records: The file record requests to be read
        '''
        ModbusRequest.__init__(self, **kwargs)
        self.records  = records or []

    def encode(self):
        ''' Encodes the request packet

        :returns: The byte encoded packet
        '''
        total_length = sum((record.record_length * 2) + 7 for record in self.records)
        packet = struct.pack('B', total_length)
        for record in self.records:
            packet += struct.pack('>BHHH', 0x06, record.file_number,
                record.record_number, record.record_length)
            packet += record.record_data
        return packet

    def decode(self, data):
        ''' Decodes the incoming request

        :param data: The data to decode into the address
        '''
        count, self.records = 1, []
        byte_count = byte2int(data[0])
        while count < byte_count:
            decoded = struct.unpack('>BHHH', data[count:count+7])
            response_length = decoded[3] * 2
            count  += response_length + 7
            record  = FileRecord(record_length=decoded[3],
                file_number=decoded[1], record_number=decoded[2],
                record_data=data[count - response_length:count])
            if decoded[0] == 0x06: self.records.append(record)

    def execute(self, context):
        ''' Run the write file record request against the context

        :param context: The datastore to request from
        :returns: The populated response
        '''
        # TODO do some new context operation here
        # if file number, record number, or address + length
        # is too big, return an error.
        return WriteFileRecordResponse(self.records)


class WriteFileRecordResponse(ModbusResponse):
    '''
    The normal response is an echo of the request.
    '''
    function_code = 0x15
    _rtu_byte_count_pos = 2

    def __init__(self, records=None, **kwargs):
        ''' Initializes a new instance

        :param records: The file record requests to be read
        '''
        ModbusResponse.__init__(self, **kwargs)
        self.records  = records or []

    def encode(self):
        ''' Encodes the response

        :returns: The byte encoded message
        '''
        total_length = sum((record.record_length * 2) + 7 for record in self.records)
        packet = struct.pack('B', total_length)
        for record in self.records:
            packet += struct.pack('>BHHH', 0x06, record.file_number,
                record.record_number, record.record_length)
            packet += record.record_data
        return packet

    def decode(self, data):
        ''' Decodes the incoming request

        :param data: The data to decode into the address
        '''
        count, self.records = 1, []
        byte_count = byte2int(data[0])
        while count < byte_count:
            decoded = struct.unpack('>BHHH', data[count:count+7])
            response_length = decoded[3] * 2
            count  += response_length + 7
            record  = FileRecord(record_length=decoded[3],
                file_number=decoded[1], record_number=decoded[2],
                record_data=data[count - response_length:count])
            if decoded[0] == 0x06: self.records.append(record)


class MaskWriteRegisterRequest(ModbusRequest):
    '''
    This function code is used to modify the contents of a specified holding
    register using a combination of an AND mask, an OR mask, and the
    register's current contents. The function can be used to set or clear
    individual bits in the register.
    '''
    function_code = 0x16
    _rtu_frame_size = 10
    

    def __init__(self, address=0x0000, and_mask=0xffff, or_mask=0x0000, **kwargs):
        ''' Initializes a new instance

        :param address: The mask pointer address (0x0000 to 0xffff)
        :param and_mask: The and bitmask to apply to the register address
        :param or_mask: The or bitmask to apply to the register address
        '''
        ModbusRequest.__init__(self, **kwargs)
        self.address  = address
        self.and_mask = and_mask
        self.or_mask  = or_mask

    def encode(self):
        ''' Encodes the request packet

        :returns: The byte encoded packet
        '''
        return struct.pack('>HHH', self.address, self.and_mask, self.or_mask)

    def decode(self, data):
        ''' Decodes the incoming request

        :param data: The data to decode into the address
        '''
        self.address, self.and_mask, self.or_mask = struct.unpack('>HHH', data)

    def execute(self, context):
        ''' Run a mask write register request against the store

        :param context: The datastore to request from
        :returns: The populated response
        '''
        if not (0x0000 <= self.and_mask <= 0xffff):
            return self.doException(merror.IllegalValue)
        if not (0x0000 <= self.or_mask <= 0xffff):
            return self.doException(merror.IllegalValue)
        if not context.validate(self.function_code, self.address, 1):
            return self.doException(merror.IllegalAddress)
        values = context.getValues(self.function_code, self.address, 1)[0]
        values = ((values & self.and_mask) | self.or_mask)
        context.setValues(self.function_code, self.address, [values])
        return MaskWriteRegisterResponse(self.address, self.and_mask, self.or_mask)


class MaskWriteRegisterResponse(ModbusResponse):
    '''
    The normal response is an echo of the request. The response is returned
    after the register has been written.
    '''
    function_code = 0x16
    _rtu_frame_size = 10

    def __init__(self, address=0x0000, and_mask=0xffff, or_mask=0x0000, **kwargs):
        ''' Initializes a new instance

        :param address: The mask pointer address (0x0000 to 0xffff)
        :param and_mask: The and bitmask applied to the register address
        :param or_mask: The or bitmask applied to the register address
        '''
        ModbusResponse.__init__(self, **kwargs)
        self.address  = address
        self.and_mask = and_mask
        self.or_mask  = or_mask

    def encode(self):
        ''' Encodes the response

        :returns: The byte encoded message
        '''
        return struct.pack('>HHH', self.address, self.and_mask, self.or_mask)

    def decode(self, data):
        ''' Decodes a the response

        :param data: The packet data to decode
        '''
        self.address, self.and_mask, self.or_mask = struct.unpack('>HHH', data)


class ReadFifoQueueRequest(ModbusRequest):
    '''
    This function code allows to read the contents of a First-In-First-Out
    (FIFO) queue of register in a remote device. The function returns a
    count of the registers in the queue, followed by the queued data.
    Up to 32 registers can be read: the count, plus up to 31 queued data
    registers.

    The queue count register is returned first, followed by the queued data
    registers.  The function reads the queue contents, but does not clear
    them.
    '''
    function_code = 0x18
    _rtu_frame_size = 6

    def __init__(self, address=0x0000, **kwargs):
        ''' Initializes a new instance

        :param address: The fifo pointer address (0x0000 to 0xffff)
        '''
        ModbusRequest.__init__(self, **kwargs)
        self.address = address
        self.values = []  # this should be added to the context

    def encode(self):
        ''' Encodes the request packet

        :returns: The byte encoded packet
        '''
        return struct.pack('>H', self.address)

    def decode(self, data):
        ''' Decodes the incoming request

        :param data: The data to decode into the address
        '''
        self.address = struct.unpack('>H', data)[0]

    def execute(self, context):
        ''' Run a read exeception status request against the store

        :param context: The datastore to request from
        :returns: The populated response
        '''
        if not (0x0000 <= self.address <= 0xffff):
            return self.doException(merror.IllegalValue)
        if len(self.values) > 31:
            return self.doException(merror.IllegalValue)
        # TODO pull the values from some context
        return ReadFifoQueueResponse(self.values)


class ReadFifoQueueResponse(ModbusResponse):
    '''
    In a normal response, the byte count shows the quantity of bytes to
    follow, including the queue count bytes and value register bytes
    (but not including the error check field).  The queue count is the
    quantity of data registers in the queue (not including the count register).

    If the queue count exceeds 31, an exception response is returned with an
    error code of 03 (Illegal Data Value).
    '''
    function_code = 0x18

    @classmethod
    def calculateRtuFrameSize(cls, buffer):
        ''' Calculates the size of the message

        :param buffer: A buffer containing the data that have been received.
        :returns: The number of bytes in the response.
        '''
        hi_byte = byte2int(buffer[2])
        lo_byte = byte2int(buffer[3])
        return (hi_byte << 16) + lo_byte + 6

    def __init__(self, values=None, **kwargs):
        ''' Initializes a new instance

        :param values: The list of values of the fifo to return
        '''
        ModbusResponse.__init__(self, **kwargs)
        self.values = values or []

    def encode(self):
        ''' Encodes the response

        :returns: The byte encoded message
        '''
        length = len(self.values) * 2
        packet = struct.pack('>HH', 2 + length, length)
        for value in self.values:
            packet += struct.pack('>H', value)
        return packet

    def decode(self, data):
        ''' Decodes a the response

        :param data: The packet data to decode
        '''
        self.values = []
        _, count = struct.unpack('>HH', data[0:4])
        for index in range(0, count - 4):
            idx = 4 + index * 2
            self.values.append(struct.unpack('>H', data[idx:idx + 2])[0])

#---------------------------------------------------------------------------#
# Exported symbols
#---------------------------------------------------------------------------#
__all__ = [
    "FileRecord",
    "ReadFileRecordRequest", "ReadFileRecordResponse",
    "WriteFileRecordRequest", "WriteFileRecordResponse",
    "MaskWriteRegisterRequest", "MaskWriteRegisterResponse",
    "ReadFifoQueueRequest", "ReadFifoQueueResponse",
]
