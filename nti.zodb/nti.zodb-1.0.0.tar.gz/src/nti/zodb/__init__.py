#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Common helpers.
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

# pylint:disable=W0212

from ZODB.interfaces import IBroken

from ZODB.POSException import POSKeyError


def readCurrent(obj, container=True):
    """
    Persistence safe wrapper around zodb connection readCurrent;
    also has some built in smarts about typical objects that need
    to be read together.
    """

    # Per notes from session_storage.py, remember to activate
    # the objects first; otherwise the serial that gets recorded
    # tends to be 0 (if we had a ghost) which immediately changes
    # which leads to falce conflicts
    try:
        obj._p_activate()
        obj._p_jar.readCurrent(obj)
    except (TypeError, AttributeError):
        pass

    if container:  # BTree containers
        try:
            data = obj._SampleContainer__data
            data._p_activate()
            data._p_jar.readCurrent(data)
        except AttributeError:
            pass
    return obj


def isBroken(obj, uid=None):
    """
    Check if the object is broken (missing or an implementation of
    :class:`ZODB.interfaces.IBroken`).

    :keyword str uid: A debugging aid, unless the obj is none,
      in which case it must be non-None to result in a True return.
      This makes no sense, so try to avoid passing objects that are None
      to this function.
    """
    if obj is None:
        msg = uid if uid is not None else ''
        logger.debug("Ignoring NULL object %s", msg)
        return uid is not None


    try:
        try:
            obj._p_activate()
        except (TypeError, AttributeError):
            pass
        return IBroken.providedBy(obj)
    except (POSKeyError, TypeError):
        # XXX: How can TypeError be raised by IBroken.providedBy?
        # Note that we only catch POSKeyError---anything else, like
        # KeyError or POSError, would be a lie. In particular, StorageError
        # is a type of POSError, which would indicate connection problems to the
        # ZODB, *not* a broken object.
        logger.debug("Ignoring broken object %s, %s", type(obj), uid)
        return True

is_broken = isBroken
