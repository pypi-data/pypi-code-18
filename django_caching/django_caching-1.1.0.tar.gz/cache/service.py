import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches

from cache.models import Invalidation

cache = caches['test'] if settings.TESTING else caches['cache_manager']


class CacheService(object):
    @classmethod
    def bulk_create_invalidation(cls, cached_objects, key, sql):
        # remove the existing invalidations
        # because this method only be called when cache miss
        # in case of memcached's memory is low, this deletion is
        # necessary, otherwise a lot of legacy invalidations will
        # be created because of quick eviction & cache miss.
        Invalidation.objects.filter(key=key).delete()

        # create new invalidations
        invs = Invalidation.objects.bulk_create([
            Invalidation(
                key=key,
                cached_object=obj,
                sql=sql,
                count=len(cached_objects),
            )
            for obj in cached_objects
        ])
        return invs

    @classmethod
    def get_invalidations(cls, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Invalidation.objects.filter(
            content_type=content_type,
            object_id=obj.id,
        )

    @classmethod
    def invalidate_cache_for(cls, obj):
        # if obj.id is not set, that means this is a new created
        # object, we need to reset the cache namespace to make
        # some queries like objects.all() work.
        if not obj.id:
            cls._reset_namespace(obj._meta.db_table)
            return

        # TODO: Think about raise condition
        # if new invalidation created when invalidating
        # what will happen?
        #
        # different with bulk_create_invalidation, we don't
        # need to remove the legacy invalidations here
        # because the removal from db may cause efficiency issue
        # why we don't have efficiency problem in bulk_create?
        # because we need *bulk* create anyway, that's already a
        # slow db query.
        invalidations = cls.get_invalidations(obj)
        keys = [i.key for i in invalidations]
        cache.delete_many(keys)
        invalidations.delete()

    # cache namespace

    @classmethod
    def _namespace_key(cls, model):
        return 'namespace::{}'.format(model)

    @classmethod
    def _reset_namespace(cls, model):
        key = cls._namespace_key(model)
        namespace = uuid.uuid4().hex
        # namespace should never expire
        cache.set(key, namespace, timeout=None)
        return namespace

    @classmethod
    def get_namespace(cls, model):
        key = cls._namespace_key(model)
        namespace = cache.get(key)
        if not namespace:
            namespace = cls._reset_namespace(model)
        return namespace
