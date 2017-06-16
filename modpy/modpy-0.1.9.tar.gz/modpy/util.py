import logging
import socket

logger = logging.getLogger(__package__)

class NetAddr:
    def __init__(self, prot, ipaddr, port):
        self.prot = prot
        self.ipaddr = ipaddr
        self.port = port


def get_outbound_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('google.com', 80))
    name = sock.getsockname()[0]
    sock.close()
    return name
    
def addr_to_netaddr(addr):
    toks = addr.split(":")
    prot = "tcp"
    if (len(toks) == 2):
        # ipaddr:port
        ipaddr = toks[0]
        port = toks[1]
    elif (len(toks) == 3):
        prot = toks[0]
        ipaddr = toks[1]
        port = toks[2]
    else:
        raise Exception("Invalid addr")

    if (prot != "tcp"):
        return Exception("Unsupported protocol")

    try:
        portn = int(port)
    except Exception as e:
        raise Exception("Invalid port")

    return NetAddr(prot, ipaddr, portn)
            
        
                     
