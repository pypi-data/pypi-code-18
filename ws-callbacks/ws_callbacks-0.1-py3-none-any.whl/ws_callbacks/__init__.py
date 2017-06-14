import asyncio

class Callbacks(object):
    def __init__(self):
        self.__callbacks = []
    
    def add_callback(self, callable_):
        self.__callbacks.append(callable_)

    def __call__(self, *args):
        for callable_ in self.__callbacks:
            callable_(*args)
    
    async def acall(self, *args):
        for callable_ in self.__callbacks:
            await callable_(*args)

