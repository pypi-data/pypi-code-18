from .mns_client import MNSClient

__version__ = '0.1.7'


def connect(ak, sk, endpoint, queue_name):
    return MNSClient(ak, sk, endpoint, queue_name)
