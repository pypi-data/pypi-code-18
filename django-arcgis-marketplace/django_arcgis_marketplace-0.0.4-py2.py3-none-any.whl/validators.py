import os
import zipfile

from django.core import exceptions
from django.utils.translation import ugettext_lazy as _


def validate_file_extension(value):
    extension = os.path.splitext(value.name)[1]

    if extension not in ('.zip',):
        raise exceptions.ValidationError(_('File extension not supported'))


def validate_zip_compression(value):
    extension = os.path.splitext(value.name)[1]

    if extension == '.zip' and\
            (not zipfile.is_zipfile(value) or
             zipfile.ZipFile(value).testzip() is not None):
        raise exceptions.ValidationError(_('.zip file error'))
