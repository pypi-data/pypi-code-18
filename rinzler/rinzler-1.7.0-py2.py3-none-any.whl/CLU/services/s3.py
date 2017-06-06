import boto3
from botocore.client import Config

from config.settings import AWS_CREDENTIALS


class S3(object):

    __s3 = None

    __bucket = None

    def __init__(self):
        self.set_s3(AWS_CREDENTIALS)

    def upload_file(self, file_data, file_key, acl='public-read'):
        self.__s3.Bucket(self.get_bucket()).put_object(Key=file_key, ACL=acl, Body=file_data)
        return True

    def get_buckets_list(self):
        bucket_list = dict()
        for bucket in self.__s3.buckets.all():
            bucket_list[bucket.name] = bucket

        return bucket_list

    def set_s3(self, config):
        self.__s3 = boto3.resource(
            's3',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            config=Config(signature_version='s3v4')
        )
        return self

    def set_bucket(self, bucket_name):
        self.__bucket = bucket_name
        return self

    def get_bucket(self):
        return self.__bucket
