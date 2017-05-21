import os.path
import zipfile

from django.db.models import FileField
from . import validators as arcgis_validators


class CompressField(FileField):
    default_validators = [
        arcgis_validators.validate_file_extension,
        arcgis_validators.validate_zip_compression
    ]

    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)
        outpath = os.path.splitext(file.path)[0]

        if not os.path.isdir(outpath) and zipfile.is_zipfile(file):
            with zipfile.ZipFile(file) as zip_file:
                zip_file.extractall(outpath)

        return file
