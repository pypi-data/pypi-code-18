import boto3
from botocore.client import Config
from cocoag.configuration.config import config


class S3Client(object):
    s3 = None

    def __init__(self):
        pass

    @classmethod
    def get_bucket_location(cls):
        """
        "When the bucket's region is US East (N. Virginia), Amazon S3 returns an empty string for the bucket's region"
        http://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETlocation.html
        """
        return cls.s3.get_bucket_location(Bucket=config.get("s3", "bucket"))["LocationConstraint"]

    @classmethod
    def get_obj_url(cls, key_name):
        cls._connect()
        bucket = config.get("s3", "bucket")
        return '%s/%s/%s' % (cls.s3.meta.endpoint_url, bucket, key_name)

    @classmethod
    def save(cls, data, key_name):
        cls._connect()
        cls.s3.put_object(
            ACL='public-read',
            Body=data,
            Bucket=config.get("s3", "bucket"),
            CacheControl='no-cache',
            ContentType='image/svg+xml',
            Key=key_name
        )

    @classmethod
    def _connect(cls):
        if not cls.s3:
            cls.s3 = boto3.client(
                's3',
                aws_access_key_id=config.get("s3", "access_key"),
                aws_secret_access_key=config.get("s3", "secret_access_key"),
                config=Config(signature_version='s3v4')
            )