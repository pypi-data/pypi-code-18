from mock import Mock
from munch import munchify as m

from s3manage.buckets import Buckets


def test_buckets_work():
    raw = [m({'name': 'valid'}), m({'name': 'valid2'}), m({'name': '1'})]
    res = Mock(**{'buckets.all.return_value': raw})
    buckets = Buckets(res, Mock())
    all_buckets = buckets.get_buckets()
    assert len(all_buckets) == 3
    assert all_buckets[0].get_name() == 'valid'
    assert all_buckets[1].get_name() == 'valid2'
    assert all_buckets[2].get_name() == '1'
    bucket = buckets.get_bucket('valid2')
    assert bucket.get_name() == 'valid2'
    bucket = buckets.get_bucket('nope')
    assert bucket is None
    valid, invalid = buckets.validate_buckets(['valid', '1', 'invalid'])
    assert len(valid) == 2
    assert len(invalid) == 1


def test_empty_buckets():
    res = Mock(**{'buckets.all.return_value': []})
    buckets = Buckets(res, Mock())
    all_buckets = buckets.get_buckets()
    assert len(all_buckets) == 0
    valid, invalid = buckets.validate_buckets(['test', 'test1'])
    assert len(valid) == 0
    assert len(invalid) == 2
    bucket = buckets.get_bucket('nope')
    assert bucket is None
