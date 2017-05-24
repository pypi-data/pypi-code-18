#!/usr/lib/env python
# -*- encoding:utf-8 -*-

import sys
import struct
import cStringIO

PROTOCOL_VERSION = 0x01
PROTOCOL_HEADER_FORMAT = "!BHI"
PROTOCOL_HEADER_LENGTH = 1 + 2 + 4


class Protocol(object):
    """
        网络交互协议
    """
    def __init__(self):
        # 协议版本号 无符号整数 1字节
        self.version = PROTOCOL_VERSION
        # 协议代码 无符号整数 2字节
        self.code = 0x00
        # 协议内容
        self.package = ""
        

    def serialize(self):
        """
            序列化协议
            protocol: 待序列化协议
        """
        return struct.pack(PROTOCOL_HEADER_FORMAT, self.version, self.code, len(self.package)) \
                + struct.pack("!%ds" % len(self.package), self.package)

        
def deserialize(buffer):
    """
        反序列化协议
        buffer: 待反序列化流
    """
    sio = cStringIO.StringIO(buffer)
    # 反序列化协议
    version, code, length = struct.unpack(PROTOCOL_HEADER_FORMAT, sio.read(PROTOCOL_HEADER_LENGTH))
    package = struct.unpack("!%ds" % length, sio.read(length))
    
    protocol = Protocol()
    protocol.version = version
    protocol.code = code
    protocol.package = package
    
    sio.close()
    return protocol


def read_from_socket(socket):
    """
        从socket连接读取协议
    """
    data = socket.recv(PROTOCOL_HEADER_LENGTH)
    if not data:
        return False

    version, code, length = struct.unpack(PROTOCOL_HEADER_FORMAT, data)
    data = socket.recv(length)
    if not data:
        return False
    
    package = struct.unpack("!%ds" % length, data)
    
    protocol = Protocol()
    protocol.version = version
    protocol.code = code
    protocol.package = package
    
    return protocol
