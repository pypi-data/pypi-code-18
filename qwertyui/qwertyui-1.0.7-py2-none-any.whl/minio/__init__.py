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
    """
    Uploads single file to minio.
    """

    size = os.stat(file_path).st_size
    file_name = os.path.split(file_path)[1]
    # TODO: can be problematic on Windows but well... I'm too lazy for this
    minio_file_path = os.path.join(minio_directory, file_name)

    with io.open(file_path, 'rb') as f:
        client.put_object(
            bucket,
            minio_file_path,
            f,
            size,
            content_type=content_type or 'application/octet-stream',
            metadata=metadata
        )

    return minio_file_path


def upload_directory(client, bucket, directory_path, minio_directory):
    """
    Uploads whole directory structure to minio (recursively).
    """

    file_paths = []

    for directory, directories, files in os.walk(directory_path):
        # TODO: can be problematic on Windows but well... I'm too lazy for this
        d = directory.replace(directory_path, '').lstrip(os.path.sep)
        destination_directory = os.path.join(minio_directory, d)

        for filename in files:
            minio_file_path = upload_file(
                client,
                bucket,
                os.path.join(directory, filename),
                destination_directory
            )
            file_paths.append(minio_file_path)

    return file_paths


def size(client, bucket, file_path):
    return client.stat_object(bucket, file_path).size
