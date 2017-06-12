from __future__ import print_function

import re
import tempfile

from .base import Base
from .hash import HASH_ALGORITHM
from .signature import SIGN_ALGORITHM


_DIRTY_PATH = re.compile('(?:^|/)(\.\.?)(?:/|$)')


class Downloader(Base):
    def _validate_entry_path(self, path):
        if path.startswith('/'):
            raise Exception(
                'Unexpected absolute entry in manifest: {}'.format(path))

        match = _DIRTY_PATH.search(path)
        if match:
            if match.group(1) == '.':
                raise Exception(
                    'Manifest entry contains redundant \'./\' segments: {}'
                    .format(path))

            raise Exception(
                'Manifest entry contains disallowed \'../\' segments: {}'
                .format(path))

    def _validate_manifest(self, manifest):
        '''Validates the manifest.

        Returns list of (hash, mode, path)-tuples for the file entries in the
        manifest.
        '''
        manifest.seek(0)

        for hash_algorithm in manifest:
            break
        else:
            raise Exception('Manifest is empty')

        if hash_algorithm[:-1].decode() != HASH_ALGORITHM:
            raise Exception(
                'Unexpected hashing algorithm in manifest: {}'
                .format(hash_algorithm[:-1]))

        entries = []
        for entry in manifest:
            if entry == b'---\n':
                break
            entries.append(entry)
        else:
            raise Exception('Manifest is not trusted: missing signature')

        for sign_algorithm in manifest:
            break
        else:
            raise Exception('Manifest is not trusted: missing signature')

        if sign_algorithm[:-1].decode() != SIGN_ALGORITHM:
            raise Exception(
                'Unexpected signing algorithm in manifest: {}'
                .format(sign_algorithm[:-1]))

        manifest_hash = self.get_hash([hash_algorithm] + entries)
        signature = b''.join(list(manifest))

        if not self.verify(manifest_hash, signature):
            raise Exception(
                'Manifest is not trusted: signature verification failed')

        result = []
        for entry in entries:
            content_hash, mode, path = entry[:-1].split(b' ', 2)

            content_hash = content_hash.decode()
            mode = int(mode, 8)
            path = path.decode()

            self._validate_entry_path(path)

            result.append((content_hash, mode, path))

        return result

    def download(self):
        with tempfile.SpooledTemporaryFile(max_size=1024*1024) as manifest:
            self.download_manifest(manifest)
            entries = self._validate_manifest(manifest)

        self.ensure_directory(self.directory)
        for content_hash, mode, path in entries:
            self.download_file(path, mode=mode, content_hash=content_hash)

    run = download
