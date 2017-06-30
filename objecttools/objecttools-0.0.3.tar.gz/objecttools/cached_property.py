import threading

from objecttools.singletons import Singleton

__all__ = ('CachedProperty', 'ThreadedCachedProperty')

_Missing = Singleton.create('_Missing', object_name='_missing')
_missing = _Missing()

_NO_DICT_ERROR = (
    'Instance "{instance!r}" of type "{type!r}" has no __dict__ attribute. '
    'If it has a __slots__ attribute, please add `__dict__` to the slots.'
)

_NO_NAME_ERROR = (
    'Cannot get name of attribute to assign to for instance "{instance!r}" of '
    'type "{type!r}".'
)

class CachedProperty(object):
    """A property that caches its return value"""
    def __init__(self, fget=None, can_set=False, can_del=False, doc=None, name=None):
        if doc is None:
            doc = getattr(fget, '__doc__', None)
        if name is None:
            name = getattr(fget, '__name__', None)
        self._getter = fget
        self._setter = bool(can_set)
        self._deleter = bool(can_del)
        if doc is not None:
            self.__doc__ = doc
        self._name = name

    @property
    def name(self):
        """The name of the attribute that this descriptor is a property for"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def getter(self, fget):
        """
        Change the getter for this descriptor to use to get the value

        :param fget: Function to call with an object as its only argument
        :type fget: Callable[[Any], Any]
        :return: self, so this can be used as a decorator like a `property`
        :rtype: CachedProperty
        """
        if getattr(self, '__doc__', None) is None:
            self.__doc__ = getattr(fget, '__doc__', None)
        if self._name is None:
            self._name = getattr(fget, '__name__', None)
        self._getter = fget
        return self

    def setter(self, can_set=None):
        """
        Like `CachedProp.deleter` is for `CachedProp.can_delete`, but for `can_set`

        :param can_set: boolean to change to it, and None to toggle
        :type can_set: Optional[bool]
        :return: self, so this can be used as a decorator like a `property`
        :rtype: CachedProperty
        """
        if can_set is None:
            self._setter = not self._setter
        else:
            self._setter = bool(can_set)
        # For use as decorator
        return self

    @property
    def can_set(self):
        """Whether this descriptor supports setting the value"""
        return self._setter

    @can_set.setter
    def can_set(self, value):
        self.setter(value)

    def deleter(self, can_delete=None):
        """
        Change if this descriptor's can be invalidated through `del obj.attr`.

        `cached_prop.deleter(True)` and::

            @cached_prop.deleter
            def cached_prop(self):
                pass

        are equivalent to `cached_prop.can_delete = True`.

        :param can_delete: boolean to change to it, and None to toggle
        :type can_delete: Optional[bool]
        :return: self, so this can be used as a decorator like a `property`
        :rtype: CachedProperty
        """
        if can_delete is None:
            self._deleter = not self._deleter
        else:
            self._deleter = bool(can_delete)
        # For use as decorator
        return self

    @property
    def can_delete(self):
        """Whether this descriptor supports invalidation through `del`"""
        return self._deleter

    @can_delete.setter
    def can_delete(self, value):
        self.deleter(value)

    def __get__(self, instance=None, owner=None):
        if instance is None:
            return self
        if self._getter is None:
            raise AttributeError('unreadable attribute')
        if self.name is not None:
            if not hasattr(instance, '__dict__'):
                try:
                    instance.__dict__ = {}
                except AttributeError:
                    pass
                if not hasattr(instance, '__dict__'):
                    raise AttributeError(_NO_DICT_ERROR.format(instance=instance, type=type(instance)))
            cached = instance.__dict__.get(self.name, _missing)
            if cached is _missing:
                cached = instance.__dict__[self.name] = self._getter(instance)
            return cached
        else:
            raise ValueError(_NO_NAME_ERROR.format(instance=instance, type=type(instance)))

    def __set__(self, instance=None, value=None):
        if instance is None:
            return self
        if not self.can_set:
            raise AttributeError('can\'t set attribute')
        if self.name is not None:
            if not hasattr(instance, '__dict__'):
                try:
                    instance.__dict__ = {}
                except AttributeError:
                    pass
                if not hasattr(instance, '__dict__'):
                    raise AttributeError(_NO_DICT_ERROR.format(instance=instance, type=type(instance)))
            instance.__dict__[self.name] = value
        else:
            raise ValueError(_NO_NAME_ERROR.format(instance=instance, type=type(instance)))

    def __delete__(self, instance=None):
        if instance is None:
            return self
        if not self.can_delete:
            raise AttributeError('can\'t delete attribute')
        if self.name is not None:
            if not hasattr(instance, '__dict__'):
                try:
                    instance.__dict__ = {}
                except AttributeError:
                    pass
                if not hasattr(instance, '__dict__'):
                    raise AttributeError(_NO_DICT_ERROR.format(instance=instance, type=type(instance)))
            instance.__dict__.pop(self.name, None)
        else:
            raise ValueError(_NO_NAME_ERROR.format(instance=instance, type=type(instance)))


class ThreadedCachedProperty(CachedProperty):
    """Thread-safe version of CachedProperty"""
    def __init__(self, fget=None, can_set=False, can_del=False,
                 doc=None, name=None, lock=threading.RLock):
        super(ThreadedCachedProperty, self).__init__(fget, can_set, can_del, doc, name)
        if callable(lock):
            lock = lock()
        self.lock = lock

    def getter(self, fget):
        with self.lock:
            return super(ThreadedCachedProperty, self).getter(fget)

    def setter(self, can_set=None):
        with self.lock:
            return super(ThreadedCachedProperty, self).setter(can_set)

    def deleter(self, can_delete=None):
        with self.lock:
            return super(ThreadedCachedProperty, self).deleter(can_delete)

    def __get__(self, instance=None, owner=None):
        with self.lock:
            return super(ThreadedCachedProperty, self).__get__(instance, owner)

    def __set__(self, instance=None, value=None):
        with self.lock:
            return super(ThreadedCachedProperty, self).__set__(instance, value)

    def __delete__(self, instance=None):
        with self.lock:
            return super(ThreadedCachedProperty, self).__delete__(instance)
