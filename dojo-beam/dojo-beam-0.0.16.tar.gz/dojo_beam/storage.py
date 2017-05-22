from __future__ import absolute_import, print_function, unicode_literals

import io
import apache_beam as beam
import googleapiclient

from googleapiclient import discovery
from apache_beam.io import ReadFromText, WriteToText, WriteToTFRecord

from dojo.storage import Storage
from dojo.vanilla.stores.google_storage import google_cloud_credentials

from .transform import ConvertTo


class BeamStorage(Storage):

    def read(self, path_or_source):
        if isinstance(path_or_source, str):
            path = path_or_source
            source = None
        else:
            path = None
            source = path_or_source
        p = self.dataset.pipeline
        if source:
            rows = (p | 'read ' + str(source) >> beam.Read(source))
        else:
            input_uri = self.as_uri(path)
            rows = (p | 'read ' + input_uri >> ReadFromText(str(input_uri)))
        return rows

    def write(self, path, rows, format='json'):
        extensions = {
            'json': '.json',
            'csv': '.csv',
            'tf': '.tfrecord.gz'
        }
        writers = {
            'json': WriteToText,
            'csv': WriteToText,
            'tf': WriteToTFRecord
        }
        extension = extensions.get(format)
        writer = writers[format]
        output_uri = self.as_uri(path)
        rows = rows | 'convert ' + output_uri + ' ' + format >> beam.ParDo(ConvertTo(format))
        rows | 'write ' + output_uri + ' ' + format >> writer(str(output_uri), file_name_suffix=extension)
        return rows

    def list_keys(self, prefix):
        raise NotImplementedError()


class BeamLocalFileStore(BeamStorage):

    def as_uri(self, path):
        return path


class BeamGoogleStorageStore(BeamStorage):

    def setup(self):
        credentials = google_cloud_credentials(self.secrets['connection'])
        self.service = discovery.build('storage', 'v1', credentials=credentials)

    def write(self, path, rows, format='json'):
        return super(BeamGoogleStorageStore, self).write(str(path), rows, format=format)

    def list_keys(self, prefix):
        req = self.service.objects().list(bucket=self.config['bucket'], prefix=prefix, delimiter='/')
        keys = []
        while req:
            resp = req.execute()
            keys += resp.get('prefixes', [])
            keys += [key['name'] for key in resp.get('items', [])]
            req = self.service.objects().list_next(req, resp)
        return keys

    def as_uri(self, path):
        return '%s://%s/%s' % (self.config['protocol'], self.config['bucket'], path)

    def read_file(self, path, file=None):
        if file is None:
            return self._read_rows(path)
        elif isinstance(file, io.BytesIO) or hasattr(file, 'read'):
            return self._read_file(path, file)
        else:
            raise ValueError('unsupported type to read file from storage', type(file))

    def _read_rows(self, key):
        file = io.BytesIO()
        req = self.service.objects().get_media(bucket=self.config['bucket'], object=key)
        downloader = googleapiclient.http.MediaIoBaseDownload(file, req)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print("Download {}%.".format(int(status.progress() * 100)))
        file.seek(0)
        rows = file.read().decode('utf-8').split('\n')
        file.close()
        return rows

    def _read_file(self, key, to_file):
        req = self.service.objects().get_media(bucket=self.config['bucket'], object=key)
        downloader = googleapiclient.http.MediaIoBaseDownload(to_file, req)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print("Download {}%.".format(int(status.progress() * 100)))
        to_file.seek(0)
        return to_file


class BeamS3Store(BeamStorage):
    pass
