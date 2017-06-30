import minio
import io
import os
import sys

from qwertyui import urlparse


def get_minio_client(url, access_key, secret_key, region='eu-central-1', bucket=None):
    """
    Wrapper for getting minio.Minio class.
    Can optionally generate a bucket if parameter is provided.
    """

    parsed = urlparse(url)
    secure = parsed.scheme == 'https'

    mc = minio.Minio(
        parsed.netloc,
        access_key,
        secret_key,
        region=region,
        secure=secure
    )

    if not bucket:
        return mc

    if not mc.bucket_exists(bucket):
        mc.make_bucket(bucket, location=region)

    return mc


def upload_file(client, bucket, file_path, minio_directory, content_type=None, metadata=None):
    size = os.stat(file_path).st_size
    file_name = os.path.split(file_path)[1]
    minio_file_path = '/'.join(minio_directory, file_name)

    with io.open(file_path, 'rb') as f:
        client.put_object(
            bucket,
            minio_file_path,
            f,
            size,
            content_type=content_type or 'application/octet-stream',
            metadata=metadata
        )


def size(client, bucket, file_path):
    return client.stat_object(bucket, file_path).size
