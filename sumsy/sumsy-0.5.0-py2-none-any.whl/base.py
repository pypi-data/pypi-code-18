import base64
import boto3
import errno
import os
import tempfile

from .hash import Hash
from .signature import Signature


__metaclass__ = type


def _read_in_chunks(reader, chunk_size=4096):
    while True:
        data = reader.read(chunk_size)
        if not data:
            break
        yield data


class Base:
    def __init__(self, config):
        self.region = config.region

        self.rsa_key = config.rsa_key

        self.bucket = config.bucket
        self.prefix = getattr(config, 'prefix', None)
        self.strip_path_components = getattr(config, 'strip', 0)
        self.manifest_key = config.manifest

        self.cache = getattr(config, 'cache', None)
        self.directory = config.directory

        if not self.directory.endswith(os.path.sep):
            self.directory += os.path.sep

        self._created_directories = set()

        self.s3 = boto3.client('s3', region_name=self.region)

    def file_entries(self):
        directory = os.path.abspath(self.directory) + os.path.sep
        for subdir, _, filenames in os.walk(directory):
            for filename in filenames:
                actual_path = os.path.join(subdir, filename)
                unrooted_path = actual_path[len(directory):]

                # Normalize separators
                if os.path.sep != '/':
                    unrooted_path = unrooted_path.replace(os.path.sep, '/')

                key = self.prefix + '/' + unrooted_path
                with open(actual_path, 'rb') as reader:
                    mode = os.fstat(reader.fileno()).st_mode & 0o777
                    yield key, mode, reader

    def sign(self, mhash):
        return base64.encodestring(Signature(self.rsa_key).sign(mhash))

    def verify(self, mhash, signature):
        return Signature(self.rsa_key).verify(
            mhash, base64.b64decode(signature))

    def get_hash(self, lines):
        h = Hash()
        for line in lines:
            h.update(line)
        return h

    def get_file_hash(self, reader):
        reader.seek(0)

        h = Hash()
        for chunk in _read_in_chunks(reader):
            h.update(chunk)
        return h

    def upload_file(self, key, reader):
        reader.seek(0)
        self.s3.upload_fileobj(reader, self.bucket, key)

    def upload_manifest(self, reader, update_latest=True):
        key = '{}.manifest'.format(self.prefix)
        self.upload_file(key, reader)

        self.s3.copy_object(
            Bucket=self.bucket,
            CopySource=dict(Bucket=self.bucket, Key=key),
            Key=self.manifest_key)

    def download_file(self, key, mode, content_hash):
        with tempfile.NamedTemporaryFile(dir=self.directory) as provisional:
            self.s3.download_fileobj(self.bucket, key, provisional)
            if content_hash != self.get_file_hash(provisional).hexdigest():
                raise Exception(
                    'File hash in manifest does not match downloaded file: {}'
                    .format(key))

            directory, _, filename = key.rpartition('/')

            for i in range(self.strip_path_components):
                directory = directory.partition('/')[2]

            if os.path.sep != '/':
                directory = directory.replace('/', os.path.sep)
            directory = os.path.join(self.directory, directory)

            self.ensure_directory(directory)

            os.fchmod(provisional.fileno(), mode)
            os.rename(provisional.name, os.path.join(directory, filename))

            try:
                provisional.close()
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

    def download_manifest(self, writer):
        self.s3.download_fileobj(self.bucket, self.manifest_key, writer)

    def ensure_directory(self, directory):
        if directory in self._created_directories:
            return

        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        self._created_directories.add(directory)
