# -*- coding: utf-8 -*-

"""
.. module:: json.encoder.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encodes a term to JSON.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import datetime
import uuid

import arrow

from pyessv._codecs.dictionary import encoder as dict_encoder
from pyessv._utils import convert
from pyessv._utils.compat import json
from pyessv._utils.compat import numeric_types
from pyessv._utils.compat import str



# Set of data types to be ignored when encoding.
_ENCODE_IGNOREABLE = tuple(list(numeric_types) + [type(None), str])

# Set of data types to be converted to string when encoding.
_ENCODE_STRING = (
    basestring,
    arrow.Arrow,
    datetime.datetime,
    uuid.UUID
    )


def encode(instance):
    """Encodes an instance of a domain model class as a JSON text blob.

    :param pyessv.Entity instance: A domain model class instance to be encoded as a JSON text blob.

    :returns: Instance encoded as a JSON text blob.
    :rtype: str

    """
    # Convert to dictionary.
    as_dict = dict_encoder.encode(instance)

    # Return JSON.
    return str(dict_to_json(as_dict))


def dict_to_json(as_dict):
    """Converts a dictionary to json.

    :param dict as_dict: A dictionary.

    :returns: A json encoded text blob.
    :rtype: str

    """
    return json.dumps(_to_encodable(as_dict), indent=4, sort_keys=True)


def _to_encodable(obj, key_formatter=convert.str_to_camel_case):
    """Converts data to encodeable representation.

    """
    if isinstance(obj, _ENCODE_IGNOREABLE):
        return obj

    elif isinstance(obj, _ENCODE_STRING):
        return str(obj)

    elif isinstance(obj, collections.Mapping):
        return {str(key_formatter(k)): _to_encodable(v) for k, v in iter(obj.items())}

    elif isinstance(obj, collections.Iterable):
        return [_to_encodable(i) for i in obj]
