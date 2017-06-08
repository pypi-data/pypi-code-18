from .mns_client import MNSClient

__version__ = '0.2.0'


def connect(ak, sk, endpoint, queue_name):
    return MNSClient(ak, sk, endpoint, queue_name)
