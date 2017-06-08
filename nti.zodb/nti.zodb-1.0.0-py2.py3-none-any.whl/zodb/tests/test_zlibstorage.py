#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_in
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import not_none

import fudge
import unittest

from nti.zodb.zlibstorage import ZlibStorageClientStorageURIResolver
from nti.zodb.zlibstorage import ZlibStorageFileStorageURIResolver

from nti.zodb.tests import SharedConfiguringTestLayer


class TestZlibStorage(unittest.TestCase):

    @fudge.patch('ZEO.ClientStorage.ClientStorage',
                 'zc.zlibstorage.ZlibStorage',
                 'ZODB.DB')
    def test_resolve_zeo(self, fudge_cstor, fudge_zstor, fudge_db):

        uri = ('zlibzeo:///dev/null/Users/jmadden/Projects/DsEnvs/AlphaExport/var/zeosocket'
               '?connection_cache_size=25000'
               '&cache_size=104857600&storage=1'
               '&database_name=Users'
               '&blob_dir=/Users/jmadden/Projects/DsEnvs/AlphaExport/data/data.fs.blobs'
               '&shared_blob_dir=True')

        _, _, kw, factory = ZlibStorageClientStorageURIResolver()(uri)

        assert_that(kw, is_({'blob_dir': '/Users/jmadden/Projects/DsEnvs/AlphaExport/data/data.fs.blobs',
                             'cache_size': 104857600,
                             'shared_blob_dir': 1,
                             'storage': '1'}))
        assert_that(factory, has_property('__name__', 'zlibfactory'))

        fudge_cstor.is_callable().returns_fake().is_a_stub()
        fudge_zstor.is_callable().returns(1)
        fudge_db.is_callable().returns(2)

        assert_that(factory(), is_(2))

    @fudge.patch('repoze.zodbconn.resolvers.FileStorage',
                 'zc.zlibstorage.ZlibStorage',
                 'repoze.zodbconn.resolvers.DB')
    def test_resolve_file(self, fudge_cstor, fudge_zstor, fudge_db):

        uri = ('zlibfile:///dev/null/Users/jmadden/Projects/DsEnvs/AlphaExport/var/zeosocket'
               '?connection_cache_size=25000'
               '&cache_size=104857600&storage=1'
               '&database_name=Users'
               '&blob_dir=/Users/jmadden/Projects/DsEnvs/AlphaExport/data/data.fs.blobs'
               '&shared_blob_dir=True')

        _, _, kw, factory = ZlibStorageFileStorageURIResolver()(uri)

        assert_that(kw, is_({}))



        assert_that(factory, has_property('__name__', 'zlibfactory'))

        fudge_cstor.is_callable().returns_fake().is_a_stub()
        fudge_zstor.is_callable().returns(1)
        fudge_db.is_callable().returns_fake().is_a_stub()

        assert_that(factory(), is_(not_none()))

    def test_install(self):
        from repoze.zodbconn import resolvers
        from nti.zodb.zlibstorage import install_zlib_client_resolver

        before = resolvers.RESOLVERS.copy()
        install_zlib_client_resolver()
        try:
            assert_that('zlibfile', is_in(resolvers.RESOLVERS))
            assert_that('zlibzeo', is_in(resolvers.RESOLVERS))
        finally:
            resolvers.RESOLVERS = before
