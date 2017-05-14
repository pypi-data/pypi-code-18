import typing


class GeneratorIterable(object):
    def __init__(self, generator: typing.Callable, *args, **kwargs) -> None:
        if not callable(generator):
            raise TypeError("Parameter 'generator' must be a generator function")
        self._generator = generator
        self._args = args
        self._kwargs = kwargs

    def __iter__(self) -> typing.Generator:
        return self._generator(*self._args, **self._kwargs)
