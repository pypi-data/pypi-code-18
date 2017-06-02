import time
import os.path
from .utils import gunzip_data


class ObjectVersionSaver(object):
    """Class for saving S3 object versions on demand.

    >>> fname_factory = FnameFactory().last_modified
    >>> saver = ObjectVersionSaver(s3, fname_factory, to_decompress)
    >>> fname, keydct = saver.save("buck", "a/b.json", "da13b")
    >>> fname, keydct = saver.save("buck", "a/b.json", "ba26c")
    >>> fname, keydct = saver.save("buck", "a/c.json", "dd112")

    fname is file name where given version was saved.
    keydct is dict as from s3.ObjectVersion(...).get()
    """
    def __init__(self, s3, fname_factory, to_decompress):
        """
        Args:
            s3 (boto3.resources.factory.s3.ServiceResource):
                >>> from boto3.session import Session
                >>> session = Session()  # use access keys, profile_name etc
                >>> s3 = session.resource("s3")
            fname_factory (func returning file name): The function takes args:
                bucket_name (str): S3 bucket name
                key_name (str): S3 object key name
                version_id (str): S3 object version identifier
                objdict (dict): dict from s3.ObjectVersion(...).get()
            to_decompress (tuple of content encodings): content encodings
                to decompress. Usually None or ("deflate", "gzip").
                Only "deflate" and "gzip" encodings supported at the moment.
        """
        self.s3 = s3
        self.fname_factory = fname_factory
        self.to_decompress = to_decompress

    def save(self, bucket_name, key_name, version_id):
        """
        Save given object version into file (created by self.fname_factory).
        Args:
            bucket_name (str): S3 bucket name
            key_name (str): S3 object key name
            version_id (str): S3 object version identifier
        Raises:
            botocore.exceptions.ClientError: when missing credentials, missing
                bucket, missing object or object version or insufficient
                permissions.
        Returns:
            tuple (fname, keydct):
                fname (str): file name
                keydct (dict): as returned from s3.ObjectVersion(...).get()
        """
        key = self.s3.ObjectVersion(bucket_name, key_name, version_id).get()
        last_modified = key["LastModified"]
        fname = self.fname_factory(bucket_name,
                                   key_name,
                                   version_id,
                                   key)
        # TODO: modify for large files into streaming
        # gzip requires .tell and key["Body"] does not provide it
        with open(fname, "wb") as f:
            if key["ContentEncoding"] in self.to_decompress:
                f.write(gunzip_data(key["Body"].read()))
            else:
                f.write(key["Body"].read())
        # set modification time to the time, version was created in bucket
        tm = time.mktime(last_modified.timetuple())
        os.utime(fname, (tm, tm))
        return fname, key


class FnameFactory(object):
    """Provide functions creating for S3 object version a file name.
    Such filename is usually used to save the content into it.

    Currently it provides two different functions:
        last_modified: name contains (not only) time of last modification.
        version_id: name contains (not only) object version_id.
    """

    def __init__(self):
        pass

    def last_modified(self, bucket_name, key_name, version_id, objdict):
        """Create for S3 object version unique file name.

        e.g.: "data.2017-05-15T22_21_07Z.json"

        Args:
            bucket_name (str): S3 bucket name
            key_name (str): S3 object key name
            version_id (str): S3 object version identifier
            objdict (dict): dict from s3.ObjectVersion(...).get()
        Returns (str): file name
        """
        basename, ext = os.path.splitext(os.path.basename(key_name))
        templ = "{basename}.{LastModified:%Y-%m-%dT%H_%M_%SZ}{ext}"
        return templ.format(basename=basename,
                            ext=ext,
                            **objdict)

    def version_id(self, bucket_name, key_name, version_id, objdict):
        """Create for S3 object version unique file name.

        e.g.: "data.d4b4cb144387dqf.json"

        Args:
            bucket_name (str): S3 bucket name
            key_name (str): S3 object key name
            version_id (str): S3 object version identifier
            objdict (dict): dict from s3.ObjectVersion(...).get()
        Returns (str): file name
        """
        basename, ext = os.path.splitext(os.path.basename(key_name))
        templ = "{basename}.{version_id}{ext}"
        return templ.format(basename=basename,
                            ext=ext,
                            version_id=version_id,
                            **objdict)
