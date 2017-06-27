# coding: utf-8
import hashlib
import logging

from django.conf import settings
from django.core.cache import caches
from django.db import models
from django.db.models.query import QuerySet
from django.db.models.sql import EmptyResultSet

from cache.constants import ONE_DAY
from cache.service import CacheService

cache = caches['test'] if settings.TESTING else caches['cache_manager']
logger = logging.getLogger(__name__)


class CachedQuerySet(QuerySet):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.get('timeout', ONE_DAY)
        if 'timeout' in kwargs:
            del kwargs['timeout']
        super(CachedQuerySet, self).__init__(*args, **kwargs)

    def get_cache_key_and_sql(self):
        sql = self._sql()
        model = self.model._meta.db_table
        key = u'{namespace}::{model}::{sql}::{db}'.format(
            namespace=CacheService.get_namespace(model),
            model=model,
            sql=sql,
            db=self.db,
        )
        return hashlib.md5(key.encode('utf-8')).hexdigest(), sql

    def _sql(self):
        clone = self.query.clone()
        sql, params = clone.get_compiler(using=self.db).as_sql()
        return sql % params

    def iterator(self):
        try:
            key, sql = self.get_cache_key_and_sql()
        # workaround for Django bug # 12717
        except EmptyResultSet:
            return

        cached_objects = cache.get(key)
        if not cached_objects:
            logger.debug('cache miss for {}'.format(key))
            cached_objects = list(super(CachedQuerySet, self).iterator())

            # be careful, if the cache value is too large and your memcached
            # is running on small memory box, the key will be evicted immediately
            # after your inserted it. So that will cause legacy invalidation creation
            # in the invalidation table
            CacheService.bulk_create_invalidation(cached_objects, key, sql)
            cache.set(key, cached_objects, timeout=self.timeout)
        else:
            logger.debug('cache hit for {}'.format(key))

        for obj in cached_objects:
            yield obj

    def bulk_create(self, *args, **kwargs):
        # TODO invalidate cached objects
        return super(CachedQuerySet, self).bulk_create(*args, **kwargs)

    def update(self, **kwargs):
        # TODO invalidate cached objects
        return super(CachedQuerySet, self).update(**kwargs)


class CacheManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.get('timeout', ONE_DAY)
        if 'timeout' in kwargs:
            del kwargs['timeout']
        super(CacheManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return CachedQuerySet(self.model, using=self._db, timeout=self.timeout)
