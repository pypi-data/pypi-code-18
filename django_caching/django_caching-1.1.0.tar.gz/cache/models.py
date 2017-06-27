from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import (
    pre_save,
    pre_delete,
    m2m_changed,
)

from cache.listeners import (
    invalidate_model_cache,
    invalidate_m2m_cache,
)


class Invalidation(models.Model):
    """
    Invalidation is for storing the cached object and the related keys
    An db object could be cached for in many queries, for example:

    1. Problem.cached_objects.get(id=1)
    2. Problem.cached_objects.get(unique_name='a-b-plus')
    3. Problem.cached_objects.all()

    we will generate three keys and store three different results in cache.
    once the object is changed, we need to invalidate the three related keys
    in the cache.

    so we can query from the Invalidation table and find the three keys.
    """

    key = models.CharField(max_length=255, help_text='cache key', db_index=True)
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, null=True)
    cached_object = GenericForeignKey('content_type', 'object_id')

    # for admin
    sql = models.TextField(null=True)
    count = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    # deprecated
    class_name = models.CharField(max_length=255, null=True)

    class Meta:
        index_together = ['content_type', 'object_id']

    def __str__(self):
        return '{}.{}.{}'.format(self.content_type, self.object_id, self.key)

    def __unicode__(self):
        return u'{}'.format(self.__str__())


pre_save.connect(invalidate_model_cache)
pre_delete.connect(invalidate_model_cache)
m2m_changed.connect(invalidate_m2m_cache)
