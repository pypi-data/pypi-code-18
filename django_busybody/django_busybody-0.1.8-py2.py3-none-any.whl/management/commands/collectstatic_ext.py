# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import json
import hashlib

from django.contrib.staticfiles.management.commands import collectstatic
from django.core.files.base import ContentFile


class Command(collectstatic.Command):
    filename = '.hashvalues_staticfiles.json'

    def _save(self, path, fileobj, max_length=None):
        self.cur_prefixed_path = path
        return self.org_save(path, fileobj, max_length)

    def __save(self, path, fileobj):
        self.hash_map[path] = hashlib.sha1(fileobj.read()).hexdigest()
        fileobj.seek(0)
        if self.prev_hash_map.get(path) == self.hash_map[path]:
            self.log("Skiping same hash '%s'" % path)
            return path
        if self.storage.exists(path):
            self.org_delete(path)
        return self._org_save(path, fileobj)

    def delete_file(self, path, p, source_storage):
        return True

    def handle(self, **options):
        self.org_save = self.storage.save
        self._org_save = self.storage._save
        self.org_delete = self.storage.delete
        if self.storage.exists(self.filename):
            with self.storage.open(self.filename, 'rb') as fp:
                self.prev_hash_map = json.loads(fp.read().decode('utf-8'))
        else:
            self.prev_hash_map = {}
        self.hash_map = {}
        self.storage.save = self._save
        self.storage._save = self.__save
        self.storage.delete = lambda *args, **kw: None
        self.storage.get_available_name = lambda name, *args, **kw: name

        super(Command, self).handle(**options)

        if self.storage.exists(self.filename):
            self.storage.delete(self.filename)
        contents = json.dumps(self.hash_map).encode('utf-8')
        self.storage.save(self.filename, ContentFile(contents))
