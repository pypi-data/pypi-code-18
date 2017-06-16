""" Messages transferred between nodes for resource access. """

import json

# message tags
MESG_CALL    = 0 # Function call
MESG_CALLNR  = 1 # Function call (no return)
MESG_RETURN  = 2 # Return from function call
MESG_CANCEL  = 3 # Cancel function call
MESG_BCAST   = 4 # Broadcast
MESG_NTAGS   = 5

# special message for internal use
IMESG_SHUTDOWN  = False

# special resource names
RESULT_OK    = '#OK#'
RESULT_ERROR = '#ERROR#'

# error codes (when resource=RESULT_ERROR)
ERROR_CONNFAIL = "Failed to Send Request"
ERROR_NOACK    = "No Acknowledgement from Server"
ERROR_TYPE     = "Type Error"


class MessageHeader:
    def __init__(self, srcaddr, destaddr, callid, noret, timeout):
        self.srcaddr = srcaddr
        self.destaddr = destaddr
        self.callid = callid
        self.noret = noret
        self.timeout = timeout

    def __str__(self):
        return "[s=%s, t=%s, cid=%d]" % (self.srcaddr,
                                         self.destaddr,
                                         self.callid)
        
class MessageBody:
    _mesg_strs = [
        'CALL',
        'CALLNB',
        'RETURN',
        'CANCEL',
        'BCAST'
    ]
    def __init__(self, tag, resource, *args):
        if (tag < 0 or tag >= MESG_NTAGS):
            raise Exception("Invalid message Tag")
        self.tag = tag
        self.resource = resource
        self.args = args

    def __str__(self):
        return "[%s, res=%s, args=%r]" % (self._mesg_strs[self.tag],
                                          self.resource, self.args)

class Message:
    def __init__(self, header, body):
        self.header = header
        self.body = body

    def set_noret(self, val):
        self.header.noret = val

    def is_noret(self):
        return self.header.noret

    def __str__(self):
        return str(self.header) + str(self.body)

def create(tag, srcaddr, destaddr, resource, *args):
    try:
        header = MessageHeader(srcaddr, destaddr, 0, 0, 0)
        body = MessageBody(tag, resource, *args)
        return Message(header, body)
    except Exception as e:
        raise e
    
class MessageCodecJSON:
    def __init__(self):
        return
        
    def decode_message(self, s):
        try:
            t = json.loads(s)
            header = MessageHeader(t[0], t[1], t[2], t[3], t[4])
            body = MessageBody(t[5], t[6], *t[7])
            return Message(header, body)
        except Exception as e:
            raise e

    def encode_message(self, m):
        try:
            h = m.header
            b = m.body
            return json.dumps([h.srcaddr, h.destaddr, h.callid,
                               h.noret, h.timeout,
                               b.tag, b.resource, b.args])
        except Exception as e:
            raise e
    
