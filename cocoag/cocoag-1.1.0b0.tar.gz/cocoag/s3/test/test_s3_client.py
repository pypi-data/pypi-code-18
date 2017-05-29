from cocoag.s3.s3_client import S3Client


def test_client_starts_as_none():
    assert not S3Client.s3