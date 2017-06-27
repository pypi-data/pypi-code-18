# coding:utf-8
import logging

logger = logging.getLogger(__name__)


def invalidate_model_cache(sender, instance, **kwargs):
    from cache.service import CacheService

    # TODO there is an assumption that we should use cached_objects
    # instead of objects. but there is not limit for this in code.
    # so if user use objects for CacheManager, the invalidation logic
    # is not correct.
    if not hasattr(instance.__class__, 'cached_objects'):
        return
    logger.debug(u'Invalidating model cache for {} {}'.format(sender, instance))
    CacheService.invalidate_cache_for(instance)


def invalidate_m2m_cache(sender, instance, model, **kwargs):
    from cache.service import CacheService

    if not hasattr(instance.__class__, 'cached_objects'):
        return
    logger.debug(u'Invalidating m2m cache for {} {} {}'.format(sender, instance, model))
    CacheService.invalidate_cache_for(instance)
