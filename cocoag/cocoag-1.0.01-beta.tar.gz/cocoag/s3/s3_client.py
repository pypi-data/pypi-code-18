import boto3
from botocore.client import Config
from cocoag.s3.settings_prod import S3_ADMIN_AWS_ACCESS_KEY
from cocoag.s3.settings_prod import S3_ADMIN_SECRET_ACCESS_KEY


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
                aws_access_key_id=S3_ADMIN_AWS_ACCESS_KEY,
                aws_secret_access_key=S3_ADMIN_SECRET_ACCESS_KEY,
                config=Config(signature_version='s3v4')
            )