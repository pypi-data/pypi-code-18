import typing
import plinq.utils as utils


class GeneratorIterable(object):
    """
    Handles generators in a similar way as other iterables
    """
    def __init__(self, generator: typing.Callable, *args, **kwargs) -> None:
        utils.check_callable(generator, name="generator")
        self._generator = generator
        self._args = args
        self._kwargs = kwargs

    def __iter__(self) -> typing.Iterator:
        return self._generator(*self._args, **self._kwargs)
