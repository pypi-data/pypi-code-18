import traceback
from abc import ABCMeta, abstractmethod


def EMPTY_ACTION():
    pass


def EMPTY_CONSUMER(t):
    pass


def ON_ERROR(err):
    if isinstance(err, tuple):
        raise err[1], None, err[2]
    else:
        raise err


def THROW_IF_FATAL(err):
    if isinstance(err, tuple):
        traceback.print_exception(*err)
        # raise err[1], None, err[2]
    else:
        pass
        # raise err


class Disposable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def dispose(self):
        raise RuntimeError("unimplemented")

    @abstractmethod
    def isDisposed(self):
        raise RuntimeError("unimplemented")


class ActionDisposable(Disposable):
    on_dispose = None

    def __init__(self, on_dispose):
        self.on_dispose = on_dispose

    def dispose(self):
        print "asdsad", self.on_dispose
        if self.on_dispose:
            self.on_dispose()
            self.on_dispose = None

    def isDisposed(self):
        return self.on_dispose is None


class Emitter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def onNext(self, t):
        raise RuntimeError("unimplemented")

    @abstractmethod
    def onError(self, err):
        raise RuntimeError("unimplemented")

    @abstractmethod
    def onComplete(self):
        raise RuntimeError("unimplemented")


from .helpers import LambdaObserver
from .helpers import LambdaSingle
from .observable import Observable, ObservableEmitter
from .observers import SingleObserver

__all__ = [ON_ERROR, Disposable, LambdaSingle, LambdaObserver, Observable, ObservableEmitter, SingleObserver]
