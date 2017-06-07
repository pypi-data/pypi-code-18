from mock import Mock

from s3manage.buckets import Bucket

MOCK_NAME = "Test Bucket"
index = {'IndexDocument': {'Suffix': 'my_index.html'}}
raw_client = Mock(**{'get_bucket_website.return_value': index})
raw_bucket = Mock(**{'objects.all.return_value' : ['1', '2']})
raw_bucket.name = MOCK_NAME


def test_bucket():
    bucket = Bucket(raw_client, raw_bucket)
    items = bucket.get_items()
    assert bucket.get_name() == MOCK_NAME
    assert len(items) == 2
    assert bucket.get_index_name() == index['IndexDocument']['Suffix']
    args = {'something': 123, 'another': 'xyz'}
    bucket.put_object(**args)
    raw_bucket.put_object.assert_called_with(**args)


def test_bucket_no_website():
    client = Mock(**{'get_bucket_website.return_value': {}})
    bucket = Bucket(client, raw_bucket)
    assert bucket.get_index_name() == 'index.html'


def test_bucket_empty():
    empty_bucket = Mock(**{'name': MOCK_NAME, 'objects.all.return_value': []})
    bucket = Bucket(raw_client, empty_bucket)
    assert len(bucket.get_items()) == 0
