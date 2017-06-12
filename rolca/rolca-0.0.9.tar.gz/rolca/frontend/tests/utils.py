# pylint: disable=missing-docstring
import os

from django.core.files.uploadedfile import SimpleUploadedFile


def get_image_field():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_name = 'photo.jpg'
    image_path = os.path.join(dir_path, 'files', image_name)
    with open(image_path, 'rb') as fn:
        image_content = fn.read()

    return SimpleUploadedFile(image_name, image_content)
