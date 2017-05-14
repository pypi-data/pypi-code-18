# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import hashlib
from six import text_type, binary_type

from django.core.files.storage import FileSystemStorage
from .overwrite import OverwriteStorageMixin


class HashedStorageMixin(object):
    def _save(self, name, content, *args, **kw):
        s = content.read()
        if isinstance(s, text_type):
            s = s.encode('UTF-8', errors='escape')
        if isinstance(name, binary_type):
            name = name.decode('UTF-8', errors='escape')
        hashv = hashlib.sha1(s).hexdigest()
        hashv = hashv[:2] + os.path.sep + hashv[2:]
        ext = os.path.splitext(name)[1]
        dirname = os.path.dirname(name)
        filename = os.path.join(dirname, hashv + ext)
        return super(HashedStorageMixin, self)._save(filename, content)


class HashedFileSystemStorage(HashedStorageMixin, OverwriteStorageMixin, FileSystemStorage):
    IGNORE_OVERWRITE = True
