from core_flavor.managers import SoftDeletableQuerySet

from polymorphic.manager import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet


__all__ = ['ItemManager']


class BaseItemManager(PolymorphicManager):
    pass


class ItemQuerySet(SoftDeletableQuerySet, PolymorphicQuerySet):
    pass


ItemManager = BaseItemManager.from_queryset(ItemQuerySet)
