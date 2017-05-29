import boto3
from botocore.client import Config
from cocoag.configuration.config import config


class S3Client(object):
    s3 = None

    def __init__(self):
        pass

    @classmethod
    def get_bucket_location(cls, bucket):
        return cls.s3.get_bucket_location(Bucket=bucket)["LocationConstraint"]

    @classmethod
    def get_obj_url(cls, bucket, key_name):
        cls._connect()
        return '%s/%s/%s' % (cls.s3.meta.endpoint_url, bucket, key_name)

    @classmethod
    def save(cls, data, bucket, key_name):
        cls._connect()
        cls.s3.put_object(
            ACL='public-read',
            Body=data,
            Bucket=bucket,
            CacheControl='no-cache',
            ContentType='image/svg+xml',
            Key=key_name
        )

    @classmethod
    def _connect(cls):
        if not cls.s3:
            cls.s3 = boto3.client(
                's3',
                aws_access_key_id=config.get("s3", "admin_aws_access_key"),
                aws_secret_access_key=config.get("s3", "admin_secret_access_key"),
                config=Config(signature_version='s3v4')
            )