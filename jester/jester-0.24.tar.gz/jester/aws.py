import boto

AWS_REGION_OREGON = "us-west-2"

class AWSConfig():
    def __init__(self, access_key_id, secret_access_key, region=AWS_REGION_OREGON):
        self.access_key_id, self.secret_access_key, self.region = access_key_id, secret_access_key, region

class S3Bucket():
    def __init__(self, bucket, aws_config):
        self.connection = boto.connect_s3(
              aws_access_key_id=aws_config.access_key_id
            , aws_secret_access_key=aws_config.secret_access_key
            , host=S3Bucket.get_host_for_region(aws_config.region)
        )

        self.bucket = self.connection.get_bucket(bucket)

    @staticmethod
    def get_host_for_region(region):
        if region == AWS_REGION_OREGON:
            return "s3-us-west-2.amazonaws.com"

    def upload(self, key, filename):
        k = boto.s3.key.Key(self.bucket, key)
        k.key = key
        rsp = k.set_contents_from_filename(filename)
        return rsp

    def download(self, key):
        k = self.bucket.get_key(key)
        return k.get_contents_as_string()