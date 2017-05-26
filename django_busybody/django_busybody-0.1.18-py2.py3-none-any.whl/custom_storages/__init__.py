# coding: utf-8
from .chain import ChainStorage  # NOQA
from .hashed import (  # NOQA
    HashedStorageMixin,
    CachedHashValueFilesMixin,
    CachedManifestFilesMixin,
    HashedFileSystemStorage
)

from .overwrite import OverwriteSystemStorage  # NOQA
try:
    from .s3 import (  # NOQA
        StaticS3Storage, ManifestFilesStaticS3Storage,
        MediaS3Storage, HashedMediaS3Storage)
except ImportError:  # pragma: no cover
    raise

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.functional import cached_property


class PrivateFileSystemStorage(FileSystemStorage):
    @cached_property
    def location(self):
        return settings.PRIVATE_MEDIA_ROOT
