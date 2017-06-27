import sys

from thrift.Thrift import TApplicationException
from thrift.Thrift import TMessageType
from thrift.Thrift import TType, TException
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport

try:
    from thrift.protocol import fastbinary
except ImportError:
    fastbinary = None

if sys.version_info.major > 2:
    xrange = range


class AbstractCls(object):
    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        raise NotImplementedError

    def validate(self):
        return

    def __repr__(self):
        try:
            L = ['%s=%r' % (key, value) for key, value in self.__dict__.iteritems()]
        except AttributeError:
            L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class UserInfo(AbstractCls):
    thrift_spec = (
        None,  # 0
        (1, TType.STRING, 'user_id', None, None,),  # 1
        (2, TType.I64, 'app_id', None, None,),  # 2
        (3, TType.STRING, 'device_id', None, None,),  # 3
        (4, TType.STRING, 'user_ip', None, None,),  # 4
        (5, TType.I32, 'city_id', None, None,),  # 5
        (6, TType.DOUBLE, 'latitude', None, None,),  # 6
        (7, TType.DOUBLE, 'longitude', None, None,),  # 7
        (8, TType.STRING, 'app_ver', None, None,),  # 8
        (9, TType.STRING, 'account_id', None, None,),  # 9
        (10, TType.STRING, 'mor_account_id', None, None,),  # 10
    )

    def __init__(self, user_id=None, app_id=None, device_id=None, user_ip=None, city_id=None, latitude=None,
                 longitude=None, app_ver=None, account_id=None, mor_account_id=None, ):
        self.user_id = user_id
        self.app_id = app_id
        self.device_id = device_id
        self.user_ip = user_ip
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.app_ver = app_ver
        self.account_id = account_id
        self.mor_account_id = mor_account_id

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.user_id = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.app_id = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.device_id = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.user_ip = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I32:
                    self.city_id = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.DOUBLE:
                    self.latitude = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.DOUBLE:
                    self.longitude = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 8:
                if ftype == TType.STRING:
                    self.app_ver = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 9:
                if ftype == TType.STRING:
                    self.account_id = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 10:
                if ftype == TType.STRING:
                    self.mor_account_id = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('UserInfo')
        if self.user_id is not None:
            oprot.writeFieldBegin('user_id', TType.STRING, 1)
            oprot.writeString(self.user_id)
            oprot.writeFieldEnd()
        if self.app_id is not None:
            oprot.writeFieldBegin('app_id', TType.I64, 2)
            oprot.writeI64(self.app_id)
            oprot.writeFieldEnd()
        if self.device_id is not None:
            oprot.writeFieldBegin('device_id', TType.STRING, 3)
            oprot.writeString(self.device_id)
            oprot.writeFieldEnd()
        if self.user_ip is not None:
            oprot.writeFieldBegin('user_ip', TType.STRING, 4)
            oprot.writeString(self.user_ip)
            oprot.writeFieldEnd()
        if self.city_id is not None:
            oprot.writeFieldBegin('city_id', TType.I32, 5)
            oprot.writeI32(self.city_id)
            oprot.writeFieldEnd()
        if self.latitude is not None:
            oprot.writeFieldBegin('latitude', TType.DOUBLE, 6)
            oprot.writeDouble(self.latitude)
            oprot.writeFieldEnd()
        if self.longitude is not None:
            oprot.writeFieldBegin('longitude', TType.DOUBLE, 7)
            oprot.writeDouble(self.longitude)
            oprot.writeFieldEnd()
        if self.app_ver is not None:
            oprot.writeFieldBegin('app_ver', TType.STRING, 8)
            oprot.writeString(self.app_ver)
            oprot.writeFieldEnd()
        if self.account_id is not None:
            oprot.writeFieldBegin('account_id', TType.STRING, 9)
            oprot.writeString(self.account_id)
            oprot.writeFieldEnd()
        if self.mor_account_id is not None:
            oprot.writeFieldBegin('mor_account_id', TType.STRING, 10)
            oprot.writeString(self.mor_account_id)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()


class Token(AbstractCls):
    thrift_spec = (
        None,  # 0
        (1, TType.STRING, 'term', None, None,),  # 1
        (2, TType.STRING, 'pos', None, None,),  # 2
        (3, TType.I32, 'pos_id', None, None,),  # 3
        (4, TType.DOUBLE, 'weight', None, None,),  # 4
    )

    def __init__(self, term=None, pos=None, pos_id=None, weight=None, ):
        self.term = term
        self.pos = pos
        self.pos_id = pos_id
        self.weight = weight

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.term = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.pos = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.pos_id = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.DOUBLE:
                    self.weight = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('Token')
        if self.term is not None:
            oprot.writeFieldBegin('term', TType.STRING, 1)
            oprot.writeString(self.term)
            oprot.writeFieldEnd()
        if self.pos is not None:
            oprot.writeFieldBegin('pos', TType.STRING, 2)
            oprot.writeString(self.pos)
            oprot.writeFieldEnd()
        if self.pos_id is not None:
            oprot.writeFieldBegin('pos_id', TType.I32, 3)
            oprot.writeI32(self.pos_id)
            oprot.writeFieldEnd()
        if self.weight is not None:
            oprot.writeFieldBegin('weight', TType.DOUBLE, 4)
            oprot.writeDouble(self.weight)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()


class Tag(AbstractCls):
    thrift_spec = (
        None,  # 0
        (1, TType.I32, 'tag', None, None,),  # 1
        (2, TType.I32, 'offset', None, None,),  # 2
        (3, TType.STRING, 'bitmap', None, None,),  # 3
        (4, TType.DOUBLE, 'weight', None, None,),  # 4
        (5, TType.STRING, 'uniform', None, None,),  # 5
        (6, TType.I32, 'length', None, None,),  # 6
    )

    def __init__(self, tag=None, offset=None, bitmap=None, weight=None, uniform=None, length=None, ):
        self.tag = tag
        self.offset = offset
        self.bitmap = bitmap
        self.weight = weight
        self.uniform = uniform
        self.length = length

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.tag = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.offset = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.bitmap = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.DOUBLE:
                    self.weight = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.STRING:
                    self.uniform = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.I32:
                    self.length = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('Tag')
        if self.tag is not None:
            oprot.writeFieldBegin('tag', TType.I32, 1)
            oprot.writeI32(self.tag)
            oprot.writeFieldEnd()
        if self.offset is not None:
            oprot.writeFieldBegin('offset', TType.I32, 2)
            oprot.writeI32(self.offset)
            oprot.writeFieldEnd()
        if self.bitmap is not None:
            oprot.writeFieldBegin('bitmap', TType.STRING, 3)
            oprot.writeString(self.bitmap)
            oprot.writeFieldEnd()
        if self.weight is not None:
            oprot.writeFieldBegin('weight', TType.DOUBLE, 4)
            oprot.writeDouble(self.weight)
            oprot.writeFieldEnd()
        if self.uniform is not None:
            oprot.writeFieldBegin('uniform', TType.STRING, 5)
            oprot.writeString(self.uniform)
            oprot.writeFieldEnd()
        if self.length is not None:
            oprot.writeFieldBegin('length', TType.I32, 6)
            oprot.writeI32(self.length)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()


class LAResult(AbstractCls):
    thrift_spec = (
        None,  # 0
        (1, TType.LIST, 'tokens', (TType.STRUCT, (Token, Token.thrift_spec)), None,),  # 1
        (2, TType.LIST, 'tags', (TType.STRUCT, (Tag, Tag.thrift_spec)), None,),  # 2
    )

    def __init__(self, tokens=None, tags=None, ):
        self.tokens = tokens
        self.tags = tags

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.LIST:
                    self.tokens = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in xrange(_size0):
                        _elem5 = Token()
                        _elem5.read(iprot)
                        self.tokens.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.tags = []
                    (_etype9, _size6) = iprot.readListBegin()
                    for _i10 in xrange(_size6):
                        _elem11 = Tag()
                        _elem11.read(iprot)
                        self.tags.append(_elem11)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('LAResult')
        if self.tokens is not None:
            oprot.writeFieldBegin('tokens', TType.LIST, 1)
            oprot.writeListBegin(TType.STRUCT, len(self.tokens))
            for iter12 in self.tokens:
                iter12.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.tags is not None:
            oprot.writeFieldBegin('tags', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.tags))
            for iter13 in self.tags:
                iter13.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()


class LAException(TException, AbstractCls):
    thrift_spec = (
        None,  # 0
        (1, TType.I32, 'err_num', None, None,),  # 1
        (2, TType.STRING, 'message', None, None,),  # 2
    )

    def __init__(self, err_num=None, message=None, ):
        self.err_num = err_num
        self.message = message

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.err_num = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.message = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('Exception')
        if self.err_num is not None:
            oprot.writeFieldBegin('err_num', TType.I32, 1)
            oprot.writeI32(self.err_num)
            oprot.writeFieldEnd()
        if self.message is not None:
            oprot.writeFieldBegin('message', TType.STRING, 2)
            oprot.writeString(self.message)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()


class LARequest(AbstractCls):
    thrift_spec = (
        None,  # 0
        (1, TType.STRING, 'query', None, None,),  # 1
        (2, TType.STRUCT, 'user_info', (UserInfo, UserInfo.thrift_spec), None,),  # 2
    )

    def __init__(self, query=None, user_info=None, ):
        self.query = query
        self.user_info = user_info

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.query = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.user_info = UserInfo()
                    self.user_info.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('LARequest')
        if self.query is not None:
            oprot.writeFieldBegin('query', TType.STRING, 1)
            oprot.writeString(self.query)
            oprot.writeFieldEnd()
        if self.user_info is not None:
            oprot.writeFieldBegin('user_info', TType.STRUCT, 2)
            self.user_info.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()


class Iface:
    def process(self, req):
        pass


class Client(Iface):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def process(self, req):
        """
        Parameters:
         - req
        """
        self.send_process(req)
        return self.recv_process()

    def send_process(self, req):
        self._oprot.writeMessageBegin('process', TMessageType.CALL, self._seqid)
        args = ProcessArgs()
        args.req = req
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_process(self):
        (fname, mtype, rseqid) = self._iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(self._iprot)
            self._iprot.readMessageEnd()
            raise x
        result = ProcessResult()
        result.read(self._iprot)
        self._iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.ex is not None:
            raise result.ex
        raise TApplicationException(TApplicationException.MISSING_RESULT, "process failed: unknown result");


class ProcessArgs:
    thrift_spec = (
        None,  # 0
        (1, TType.STRUCT, 'req', (LARequest, LARequest.thrift_spec), None,),  # 1
    )

    def __init__(self, req=None, ):
        self.req = req

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.req = LARequest()
                    self.req.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('process_args')
        if self.req is not None:
            oprot.writeFieldBegin('req', TType.STRUCT, 1)
            self.req.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        try:
            L = ['%s=%r' % (key, value) for key, value in self.__dict__.iteritems()]
        except AttributeError:
            L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class ProcessResult:
    """
    Attributes:
     - success
     - ex
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (LAResult, LAResult.thrift_spec), None,),  # 0
        (1, TType.STRUCT, 'ex', (LAException, LAException.thrift_spec), None,),  # 1
    )

    def __init__(self, success=None, ex=None, ):
        self.success = success
        self.ex = ex

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = LAResult()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.ex = LAException()
                    self.ex.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('process_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.ex is not None:
            oprot.writeFieldBegin('ex', TType.STRUCT, 1)
            self.ex.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        try:
            L = ['%s=%r' % (key, value) for key, value in self.__dict__.iteritems()]
        except AttributeError:
            L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

