# -*- coding: utf-8 -*-
"""Convert many serialization formats to many formats"""

import logging

from .utils import get_package_version

from .serializer import Serializer, get_serializers, get_serializer, serialize, deserialize

__author__ = """Nick Allen"""
__email__ = 'nick.allen.cse@gmail.com'
__version__ = get_package_version()
__all__ = ['Serializer', 'get_serializers', 'get_serializer', 'serialize', 'deserialize']

logging.getLogger(__name__).addHandler(logging.NullHandler())
