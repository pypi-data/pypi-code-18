try:
    # 3.6 or greater
    from typing import ContextManager
except ImportError:  # pragma: no cover
    # <3.6 we create a ContextManager TypeHint

    # We implement the AbstractContextManager abc and
    # create the ContextManager class for TypeHint's
    # This is taken directly from the standard lib(s)
    import abc
    from typing import Generic, TypeVar

    class AbstractContextManager(abc.ABC):
        """An abstract base class for context managers."""

        def __enter__(self):
            return self

        @abc.abstractmethod
        def __exit__(self, exc_type, exc_value, traceback):
            return None

        @classmethod
        def __subclasshook__(cls, Cls):
            if cls is AbstractContextManager:
                if (any('__enter__' in B.__dict__ for B in Cls.__mro__) and
                        any('__exit__' in B.__dict__ for B in Cls.__mro__)):
                    return True
            return NotImplemented

    T_co = TypeVar('T_co', covariant=True)

    class ContextManager(Generic[T_co], extra=AbstractContextManager):

        __slots__ = ()


__all__ = (
    'ContextManager',
)
