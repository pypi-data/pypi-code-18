from __future__ import print_function

import tempfile

from .base import Base
from .hash import HASH_ALGORITHM
from .signature import SIGN_ALGORITHM


class Uploader(Base):
    def upload(self):
        if not self.rsa_key.has_private():
            raise Exception(
                'Private key is needed to sign manifest of uploaded files')

        with tempfile.TemporaryFile(
                prefix='sumsy', suffix='.manifest') as manifest:

            manifest.write('{}\n'.format(HASH_ALGORITHM).encode('utf-8'))

            # Calculate hashes, upload files
            for key, mode, reader in self.file_entries():
                manifest.write(
                    '{} 0{:o} {}\n'.format(
                        self.get_file_hash(reader).hexdigest(), mode, key)
                    .encode('utf-8'))

                print('Uploading {}'.format(key))
                self.upload_file(key, reader)

            # Sign manifest
            manifest_hash = self.get_file_hash(manifest)
            signature = self.sign(manifest_hash)

            manifest.write(
                '---\n'
                '{}\n'
                .format(SIGN_ALGORITHM)
                .encode('utf-8'))
            manifest.write(signature)

            # Upload manifest and update latest
            print('Uploading manifest')
            self.upload_manifest(manifest)

    run = upload
