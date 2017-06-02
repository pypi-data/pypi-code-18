import os
import re
from functools import reduce

import six

#  Utilities


def deepcopy(d1):
    """
    Copy recursively an a dictionary a list and all its subobject.
    """
    if isinstance(d1, dict):
        d = dict(d1)
        for i in list(d.keys()):
            d[i] = deepcopy(d[i])
        return d
    elif isinstance(d1, list):
        return list(map(deepcopy, d1))
    return d1


def recupdate(d1, d2):
    """
    Update a dictionary and its subobjects.
    """
    d = deepcopy(d1)
    for i in list(d2.items()):
        if i[0] not in d:
            d[i[0]] = deepcopy(i[1])
        else:
            if isinstance(d[i[0]], dict) and isinstance(i[1], dict):
                d[i[0]] = recupdate(d[i[0]], i[1])
            else:
                d[i[0]] = deepcopy(i[1])
    return d


def readlinkabs(l):
    """
    Resolve symlinks and make paths absolute.
    """
    while os.path.islink(l):
        p = os.readlink(l)
        if '/' not in p:
            p = os.path.join(os.path.dirname(l), p)
        l = os.path.abspath(p)
    return os.path.abspath(l)


def xhasattr(object, path):
    """
    Same has hasattr but can recurse through dict.
    """
    try:
        xgetattr(object, path)
    except (AttributeError, KeyError):
        return False
    return True


def xgetattr(object, path):
    """
    Same has getattr but can recurse through dict.
    """
    r = reduce(
        lambda x, y: (
            x.__getitem__(y) if (
                hasattr(
                    x, "__getitem__")) else getattr(
                x, y)), path.split("."), object)
    if (callable(r)):
        r = r()
    return r


def rec_rep(d, v, r):
    """
    Recursive replace.

    Replace all the instances of text in an object.
    """
    if isinstance(d, dict):
        rd = {}

        for i in d.items():
            if isinstance(i[0], six.string_types):
                k = i[0].replace(v, r)
            else:
                k = i[0]
            if isinstance(i[1], six.string_types):
                rd[k] = i[1].replace(v, r)
            elif isinstance(i[1], list):
                rd[k] = rec_rep(i[1], v, r)
            elif isinstance(i[1], dict):
                rd[k] = rec_rep(i[1], v, r)
            else:
                rd[k] = i[1]

        return rd

    if isinstance(d, list):
        rd = []

        for i in d:
            if isinstance(i, six.string_types):
                rd.append(i.replace(v, r))
            elif isinstance(i, list):
                rd.append(rec_rep(i, v, r))
            elif isinstance(i, dict):
                rd.append(rec_rep(i, v, r))
            else:
                rd.append(i)
        return rd

    assert (False)


def soft_update(d1, d2):
    """Update a dictionary without overwriting values."""
    if "@can_update" in d1:
        can_update_expr = d1["@can_update"]

        def can_upda_te(k):
            return re.match(can_update_expr, k)
    else:
        def can_update(k):
            return True

    for k in d2.keys():
        if can_update(k):
            if k not in d1:
                d1[k] = d2[k]
            else:
                if isinstance(d1[k], dict) and isinstance(d2[k], dict):
                    d1[k] = soft_update(d1[k], d2[k])
    return d1
