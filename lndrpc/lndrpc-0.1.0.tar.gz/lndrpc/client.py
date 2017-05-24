from __future__ import print_function

from .lnd import Lnd

def test_connect(lightning_node_ip, lightning_node_grpc_port):
    lnd_address = '{}:{}'.format(lightning_node_ip, lightning_node_grpc_port)
    lnd = Lnd(address=lnd_address)
    print(lnd.get_info())
