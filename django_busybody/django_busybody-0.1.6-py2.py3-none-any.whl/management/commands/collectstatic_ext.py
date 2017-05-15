# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import json
import hashlib

from django.contrib.staticfiles.management.commands import collectstatic
from django.core.files.base import ContentFile


class Command(collectstatic.Command):
    filename = '.hashvalues_staticfiles.json'

    def handle(self, **options):
        if self.storage.exists(self.filename):
            with self.storage.open(self.filename, 'rb') as fp:
                self.hash_map = json.loads(fp.read().decode('utf-8'))
        else:
            self.hash_map = {}

        super(Command, self).handle(**options)

        if self.storage.exists(self.filename):
            self.storage.delete(self.filename)
        contents = json.dumps(self.hash_map).encode('utf-8')
        self.storage._save(self.filename, ContentFile(contents))

    def copy_file(self, path, prefixed_path, source_storage):
        """
        Attempt to copy ``path`` with storage
        """
        # Skip this file if it was already copied earlier
        if prefixed_path in self.copied_files:
            return self.log("Skipping '%s' (already copied earlier)" % path)  # pragma: no cover

        with source_storage.open(path, 'rb') as source_file:
            hash_value = hashlib.sha1(source_file.read()).hexdigest()
        if self.hash_map.get(prefixed_path, '') == hash_value:
            return self.log("Skipping '%s' (hash value is same)" % path)
        self.hash_map[prefixed_path] = hash_value

        # Delete the target file if needed or break
        if not self.delete_file(path, prefixed_path, source_storage):  # pragma: no cover
            return
        # The full path of the source file
        source_path = source_storage.path(path)
        # Finally start copying
        if self.dry_run:
            self.log("Pretending to copy '%s'" % source_path, level=1)
        else:
            self.log("Copying '%s'" % source_path, level=1)
            with source_storage.open(path) as source_file:
                self.storage.save(prefixed_path, source_file)
        self.copied_files.append(prefixed_path)
