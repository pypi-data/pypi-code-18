#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Data URI base64 helper string class, designed for HTML/CSS/JS and images."""


import os
import re
import textwrap

from base64 import urlsafe_b64decode, urlsafe_b64encode
from mimetypes import guess_type
from shutil import which
from subprocess import run
from tempfile import NamedTemporaryFile
from typing import NamedTuple
from urllib.parse import quote_plus, unquote_plus
from urllib.request import urlretrieve


MIMETYPE_REGEX = r'[\w]+\/[\w\-\+\.]+'
_MIMETYPE_RE = re.compile('^{0}$'.format(MIMETYPE_REGEX))
CHARSET_REGEX = r'[\w\-\+\.]+'
DATA_URI_REGEX = (
    r'data:' +
    r'(?P<mimetype>{0})?'.format(MIMETYPE_REGEX) +
    r'(?:\;charset\=(?P<charset>{0}))?'.format(CHARSET_REGEX) +
    r'(?P<base64>\;base64)?' +
    r',(?P<data>.*)')
_DATA_URI_RE = re.compile(r'^{0}$'.format(DATA_URI_REGEX), re.DOTALL)
_EXTENSIONS = (".png", ".jpeg", ".jpg", ".tiff")  # WEBP-to-WEBP is Ok tho.


def img2webp(image_path, webp_path=None, preset="text"):
    """Try to convert Image to WEBP for max performance."""
    if not which("cwebp") or not image_path.lower().endswith(_EXTENSIONS):
        return image_path  # CWEBP is not installed, return the same image.
    image_path, preset = os.path.abspath(image_path), preset.lower().strip()
    webp_path = webp_path if webp_path else image_path + ".webp"
    if preset not in "default photo picture drawing icon text":
        preset = "text"  # Text Preset is still Ok,looks like JPG,but tiny.
    command = "{cwebp} -preset {preset} {yn} -o {out}".format(
        cwebp=which("cwebp"), preset=preset, yn=image_path, out=webp_path)
    return image_path if run(
        command, shell=True, timeout=9).returncode else webp_path


class DataURI(str):

    """Data URI Base64 string, designed for Images, WebP autoconversion."""

    @classmethod
    def make(cls, mimetype, base64, data):
        """Make a new Data URI Base64 string from arguments."""
        parts = ['data:']
        if mimetype is not None:
            if not _MIMETYPE_RE.match(mimetype):
                raise ValueError("Invalid mimetype: {0}.".format(mimetype))
            parts.append(mimetype)
            parts.append(';charset=utf-8')
        if base64:
            parts.append(';base64')
            encoded_data = urlsafe_b64encode(data).decode("utf-8")
        else:
            encoded_data = quote_plus(data)
        parts.extend([',', encoded_data])
        return cls(''.join(parts))

    @classmethod
    def from_file(cls, filename, base64=True, webp=True):
        """Make a new Data URI Base64 string from a file."""
        filename = os.path.abspath(filename)
        if webp and which("cwebp") and filename.lower().endswith(_EXTENSIONS):
            filename = img2webp(filename)
        mimetype = guess_type(filename, strict=False)[0]
        with open(filename, "rb") as fp:
            data = fp.read()
        return cls.make(mimetype, base64, data)

    @classmethod
    def from_url(cls, url, base64=True, webp=True):
        """Make a new Data URI Base64 string from a remote HTTP URL."""
        temp = NamedTemporaryFile(suffix=os.path.basename(url)).name
        return cls.from_file(urlretrieve(url, temp)[0],
                             base64=base64, webp=webp)

    def __new__(cls, *args, **kwargs):
        """Make a new Data URI Base64 string from arguments."""
        uri = super(DataURI, cls).__new__(cls, *args, **kwargs)
        uri._parse  # Trigger any ValueErrors on instantiation.
        return uri

    def __repr__(self):
        """Represent as string the Data URI Base64."""
        return 'DataURI({0})'.format(super(DataURI, self).__repr__(), )

    def wrap(self, width=80, newline="\n"):
        """Wrap Data URI Base64 string based on arguments using textwrap."""
        return type(self)(newline.join(textwrap.wrap(self, int(width))))

    @property
    def mimetype(self):
        """Return the file MIME Type of the Data URI Base64 string."""
        return self._parse.mimetype

    @property
    def charset(self):
        """Return the file Encoding of the Data URI Base64 string. UTF-8."""
        return "utf-8"

    @property
    def is_base64(self):
        """Return True if its Base64."""
        return self._parse.is_base64

    @property
    def data(self):
        """Return the raw Binary Data of the Data URI Base64 string."""
        return self._parse.data

    @property
    def _parse(self):
        """Auxiliary property method for attributes and parsing."""
        match = _DATA_URI_RE.match(self)
        if not match:
            raise ValueError("Not a valid Data URI: {0}".format(self))
        mimetype = match.group('mimetype') or None
        if match.group('base64'):
            data = urlsafe_b64decode(match.group('data').encode("utf-8"))
        else:
            data = unquote_plus(match.group('data'))
        typed_tuple = NamedTuple(
            'DataURI',
            (('mimetype', str), ('is_base64', bool), ('data', bytes)))
        return typed_tuple(mimetype, bool(match.group('base64')), data)
