#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for working with zc.zlibstorage.

TODO: Add support for zodburi, which can be installed automatically
as entry points in setup.py.
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os

from repoze.zodbconn import resolvers


class ZlibStorageClientStorageURIResolver(resolvers.ClientStorageURIResolver):
    """
    Wraps :class:`ZEO.ClientStorage.ClientStorage`
    with zc.zlibstorage when using the ``zlibzeo`` URI scheme.
    """

    def __call__(self, uri):
        # Defer these imports until we are actually used
        from ZODB import DB
        from zc.zlibstorage import ZlibStorage
        from ZODB.DemoStorage import DemoStorage
        from ZEO.ClientStorage import ClientStorage

        # It expect to find 'zeo' so make that happen
        uri = uri.replace('zlibzeo://', 'zeo://')
        key, args, storage_kw, _ = \
            super(ZlibStorageClientStorageURIResolver, self).__call__(uri)

        # key = (args, tuple(kw items), tuple(dbkw items))
        dbkw = dict(key[2])
        orig_kw = dict(key[1])

        def zlibfactory():
            # Wraps uri in :class:`zc.slibstorage.ZlibStorage` and returns a
            # :class:`ZODB.DB`

            # Delay setting the client name until the very end so whatever is going to
            # set environment variables will have done so.
            if 'client' not in storage_kw:
                name = os.environ.get("DATASERVER_ZEO_CLIENT_NAME")
                if name: # pragma: no cover This isn't documented.
                    # storage name is automatically part of it
                    storage_kw['client'] = name
            # ClientCache docs say 200MB is good
            storage_kw.setdefault('cache_size', 200 * 1024 * 1024)

            # Client storage is very picky: a Unix path must be bytes, not
            # unicode
            client = ClientStorage(*args, **storage_kw)
            if 'demostorage' in orig_kw:  # pragma: no cover
                client = DemoStorage(base=client)

            zlib = ZlibStorage(client)
            return DB(zlib, **dbkw)

        return key, args, storage_kw, zlibfactory


class ZlibStorageFileStorageURIResolver(resolvers.FileStorageURIResolver):
    """
    Wraps :class:`ZODB.FileStorage.FileStorage` with zc.zlibstorage
    when using the ``zlibfile`` URI scheme.
    """

    def __call__(self, uri):
        from zc.zlibstorage import ZlibStorage

        # It expect to find 'file' so make that happen
        uri = uri.replace('zlibfile://', 'file://')
        key, args, storage_kw, _factory = \
            super(ZlibStorageFileStorageURIResolver, self).__call__(uri)

        def zlibfactory():
            db = _factory()
            db.storage = ZlibStorage(db.storage)
            return db

        return key, args, storage_kw, zlibfactory


def install_zlib_client_resolver():
    """
    Makes it possible for :func:`repoze.zodbconn.uri.db_from_uri` to connect
    to ZEO servers that are using zlib storage, through providing support for the
    use of the ``zlibzeo`` URI scheme, and likewise for ``zlibfile://``.

    Alternatively, you can use a ZConfig file and the zconfig:// URI scheme.
    """
    # The alternative to all this is to use a ZConfig file and ZConfig URI.
    resolvers.RESOLVERS['zlibfile'] = ZlibStorageFileStorageURIResolver()
    resolvers.RESOLVERS['zlibzeo'] = ZlibStorageClientStorageURIResolver()
