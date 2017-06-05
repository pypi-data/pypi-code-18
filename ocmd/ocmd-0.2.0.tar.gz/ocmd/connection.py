from tinys3 import Connection as TinyConn, request_factory
from aliyunauth import OssAuth


request_factory.XML_PARSE_STRING = "{0}"


class Connection(TinyConn):
    def __init__(
        self, access_key, secret_key,
        default_bucket=None, tls=True,
        endpoint="oss-cn-hangzhou.aliyuncs.com"
    ):
        self.default_bucket = default_bucket
        self.auth = OssAuth(default_bucket, access_key, secret_key)
        self.tls = True
        self.endpoint = endpoint
