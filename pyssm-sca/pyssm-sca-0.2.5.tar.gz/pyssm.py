import boto3
from botocore.exceptions import ClientError
from time import time


class SSMParam(object):
    _value = None
    try:
        ssm = boto3.client('ssm')
    except ClientError as e:
        print("WARNING: AWS credentials not set. All calls will error or return the default argument if given.")
        ssm = None
    expires_at = float('inf')

    def __init__(self, name, cache_for_ms=None, raise_if_null=True, default=None):
        self.name = name
        self.cache_for_ms = cache_for_ms
        self.default = default
        self.raise_if_null = raise_if_null

    @property
    def value(self):
        if self._value is None or self.expires_at <= time() * 1000:
            self._value = self._fetch()
            self._reset_clock()
        return self._value

    def _reset_clock(self):
        self.expires_at = time() * 1000 + self.cache_for_ms if self.cache_for_ms is not None else float('inf')

    def _fetch(self):
        self._value = None
        try:
            return self.ssm.get_parameter(Name=self.name, WithDecryption=True)["Parameter"]["Value"]
        except ClientError as e:
            if self.default is None and self.raise_if_null:
                raise e
            else:
                return self.default
