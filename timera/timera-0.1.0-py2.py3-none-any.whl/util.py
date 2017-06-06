# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import datetime
import logging

try:
    # noinspection PyCompatibility
    from urlparse import urlparse
except ImportError:
    # noinspection PyUnresolvedReferences
    from urllib.parse import urlparse

log = logging.getLogger(__name__)


try:
    basestring
    def is_str(o):
        return isinstance(o, basestring)
except NameError:
    def is_str(o):
        return isinstance(o, str)


def get_unix_now(dt=None, utc=False):
    """return current time in seconds since epoch or diff of dt from now if provided"""
    now = datetime.datetime.utcnow() if utc else datetime.datetime.now()
    if dt is not None:
        return int((now - dt).total_seconds())
    else:
        epoch = datetime.datetime.utcfromtimestamp(0) if utc else datetime.datetime.fromtimestamp(0)
        return int((now - epoch).total_seconds())


def get_iso_time():
    """return iso time string in utc: 2009-01-21T22:24:18Z"""
    # '2014-05-18T20:01:23.752349'
    piso = datetime.datetime.utcnow().isoformat()
    # don't leak fractional seconds
    return piso.split('.', 1)[0] + 'Z'


def asbool(obj):
    """stolen from Paste"""
    if is_str(obj):
        obj = obj.strip().lower()
        if obj in ['true', 'yes', 'on', 'y', 't', '1']:
            return True
        elif obj in ['false', 'no', 'off', 'n', 'f', '0']:
            return False
        else:
            raise ValueError("String is not true/false: %r" % obj)
    return bool(obj)


def parse_url(url):
    parsed = urlparse(url)
    return parsed


def delete_proxy_env():
    """Delete proxy vars from environment that may influence behavior.
    https://docs.python.org/2/library/os.html?highlight=os.environ#os.environ
    When unsetenv() is supported, deletion of items in os.environ is automatically translated
    into a corresponding call to unsetenv(); however, calls to unsetenv() don't update os.environ,
    so it is actually preferable to delete items of os.environ.
    Availability: most flavors of Unix, Windows.
    """
    keys = [ 'no_proxy', 'NO_PROXY', 'http_proxy', 'HTTP_PROXY', 'https_proxy', 'HTTPS_PROXY' ]
    for key in keys:
        if key in os.environ:
            del os.environ[key]
