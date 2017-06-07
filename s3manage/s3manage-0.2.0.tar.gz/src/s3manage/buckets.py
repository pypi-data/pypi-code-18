from __future__ import print_function

import boto3


class Buckets(object):
    """
    Represents an Amazon S3 account, and provides operations on the buckets in
    various ways.
    """
    def __init__(self,
                 res=boto3.resource('s3'),
                 client=boto3.client('s3')):
        self._res = res
        self._client = client
        self._buckets = [Bucket(self._client, bucket) for bucket in
                         self._res.buckets.all()]

    def get_buckets(self):
        """
        Fetch back all of the s3 buckets, wrapped in our own helper class.

        :returns: Array of all buckets
        """
        return self._buckets

    def get_bucket(self, name):
        """
        Get a single wrapper object for the bucket with the given name.

        :return: A Bucket of the given name. None if no such bucket exists.
        """
        for bucket in self.get_buckets():
            if bucket.get_name() == name:
                return bucket
        return None

    def validate_buckets(self, buckets):
        '''
        Tests to be sure that all the buckets in the provided list are
        available on the s3 client specified.

        :param buckets: An iterable of names to check for bucket status
        :returns: (valid, invalid) tuple of iterables of buckets that are valid
        vs names that are invalid
        '''
        # This is 2*n^2, but it makes for prettier code. If your number of
        # buckets is really that high, then we can discuss making this more
        # n^2 or even look at a linear option
        present = [self.get_bucket(b) for b in buckets if self.get_bucket(b)]
        missing = [b for b in buckets if not self.get_bucket(b)]
        return present, missing


class Bucket(object):
    """
    Represents a single bucket, and wraps some functionality not provided by
    the underlying bucket object.
    """
    def __init__(self, client, bucket):
        self._client = client
        self._bucket = bucket

    def get_name(self):
        """
        Get the name of the bucket

        :returns: The string name of the bucket, as reported by S3
        """
        return self._bucket.name

    def get_index_name(self):
        """
        Gets the name of the configured Index file for this bucket

        :returns: The name of the index file for this bucket
        """
        config = self._client.get_bucket_website(Bucket=self.get_name())
        if 'IndexDocument' not in config:
            print("Bucket not configured for website, assuming " +
                  "'index.html'")
            return 'index.html'
        else:
            return config['IndexDocument']['Suffix']

    def get_items(self):
        """
        Fetch a listing of all the items in this bucket.

        :return: Array of objects in this bucket. The 'key' element on each
        item is the name of that object.
        """
        return [o for o in self._bucket.objects.all()]

    def put_object(self, **kargs):
        self._bucket.put_object(**kargs)
