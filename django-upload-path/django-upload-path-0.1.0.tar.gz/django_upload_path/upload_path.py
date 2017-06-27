# -*- encoding: utf-8 -*-
# ! python3

import inspect
import os
import os.path
import pathlib
import uuid
from typing import Tuple

from django.utils.text import slugify

SEPARATOR = '-'  # type: str

__all__ = [
    'get_safe_path_name',
    'get_base_dir_from_object',
    'parse_filename',
    'upload_path',
    'upload_path_uuid4',
    'upload_path_strip_uuid4'
]


def get_safe_path_name(filename: str) -> str:
    return slugify(filename).lower().strip()


def get_base_dir_from_object(instance):
    if inspect.isclass(instance):
        # We have model class
        base_dir = get_safe_path_name(instance.__name__)
    else:
        # We have object, NOT class
        base_dir = get_safe_path_name(instance.__class__.__name__)

    return base_dir


def parse_filename(filename: str) -> Tuple[str, str]:
    path = pathlib.Path(filename)  # type: pathlib.Path

    return path.stem, path.suffix.lower()


def upload_path(instance, filename: str) -> str:
    """
    Gets upload path in this format: {MODEL_NAME}/{SAFE_UPLOADED_FILENAME}{SUFFIX}.

    :param instance: Instance of model or model class.
    :param filename: Uploaded file name.
    :return: Target upload path.
    """
    stem, suffix = parse_filename(filename)
    base_dir = get_base_dir_from_object(instance)
    target_filename = get_safe_path_name(stem)

    return os.path.join(base_dir, "{target_filename}{suffix}".format(target_filename=target_filename,
                                                                     suffix=suffix))


def upload_path_uuid4(instance, filename: str) -> str:
    """
    Gets upload path in this format: {MODEL_NAME}/{SAFE_UPLOADED_FILENAME}{SEPARATOR}{UUID4}{SUFFIX}.
    Use this function to prevent any collisions with existing files in same folder.

    :param instance: Instance of model or model class.
    :param filename: Uploaded file name.
    :return: Target upload path.
    """
    stem, suffix = parse_filename(filename)
    base_dir = get_base_dir_from_object(instance)
    target_filename = get_safe_path_name(stem)
    rand_uuid = uuid.uuid4()

    return os.path.join(base_dir, "{target_filename}{SEPARATOR}{rand_uuid}{suffix}".format(target_filename=target_filename,
                                                                                           SEPARATOR=SEPARATOR,
                                                                                           rand_uuid=rand_uuid,
                                                                                           suffix=suffix))


def upload_path_strip_uuid4(instance, filename: str) -> str:
    """
    Gets upload path in this format: {MODEL_NAME}/{UUID4}{SUFFIX}.
    Same as `upload_path_uuid4` but deletes the original file name from the user.

    :param instance: Instance of model or model class.
    :param filename: Uploaded file name.
    :return: Target upload path.
    """
    _, suffix = parse_filename(filename)
    base_dir = get_base_dir_from_object(instance)
    rand_uuid = uuid.uuid4()

    return os.path.join(base_dir, "{rand_uuid}{suffix}".format(rand_uuid=rand_uuid,
                                                               suffix=suffix))
