import collections
import sys
from abc import ABCMeta, abstractmethod

from singles import Single
from . import Emitter, EMPTY_ACTION, Disposable, EMPTY_CONSUMER, THROW_IF_FATAL
from .helpers import LambdaObserver
from .observers import Observer, BasicObserver, SingleObserver, BlockingObserver

from multiprocessing import queues


class ObservableSource(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def subscribe(self, observer):
        raise RuntimeError("unimplemented")


class ObservableEmitter(Emitter):
    __metaclass__ = ABCMeta

    @abstractmethod
    def setDisposable(self, d):
        """

        :type d: Disposable
        """
        raise RuntimeError("unimplemented")

    @abstractmethod
    def isDisposed(self):
        raise RuntimeError("unimplemented")


def acceptFull(v, observer):
    if v == BlockingObserver.COMPLETE:
        observer.onComplete()
        return True
    elif isinstance(v, Exception):
        observer.onError(v)
        return True
    observer.onNext(v)
    return False


class ObservableBlockingSubscribe(object):
    @staticmethod
    def subscribe(source, observer):
        """

        :type observer: Observer
        :type source: ObservableSource
        """
        assert isinstance(source, ObservableSource), "source must be ObservableSource but %s" % type(source)
        assert isinstance(observer, Observer), "observer must be Observer but %s" % type(observer)

        queue = queues.Queue()

        bs = BlockingObserver(queue)
        observer.onSubscribe(bs)

        source.subscribe(bs)

        while not bs.isDisposed():
            try:
                v = queue.get(timeout=1)
            except queues.Empty:
                pass

            if bs.isDisposed() or v == BlockingObserver.TERMINATED or acceptFull(v, observer):
                break


class Observable(ObservableSource):
    source = None

    def __init__(self, source):
        """
        
        :param ObservableSource source: 
        """
        assert isinstance(source, ObservableSource), "must be ObservableSource but %s" % source
        self.source = source

    @staticmethod
    def create(on_subscribe):
        return ObservableCreate(ObservableOnSubscribe.create(on_subscribe))

    @staticmethod
    def from_(iterable):
        def from_list(emitter):
            for i in iterable:
                emitter.onNext(i)
            emitter.onComplete()

        return ObservableCreate(ObservableOnSubscribe.create(from_list))

    def subscribe(self, observer):
        assert isinstance(observer, Observer)
        observer.onSubscribe(self)

    def blockingSubscribe(self, on_next=EMPTY_CONSUMER, on_error=EMPTY_CONSUMER, on_complete=EMPTY_ACTION):
        return ObservableBlockingSubscribe.subscribe(self, LambdaObserver(on_next, on_error, on_complete))

    def map(self, func):
        return ObservableMap(self, func)

    def flatMap(self, mapper_func, maxConcurrency=1, bufferSize=128):
        return ObservableFlatMap(self, mapper_func, maxConcurrency, bufferSize)

    def doOnNext(self, func):
        return self.doOnEach(on_next=func, on_error=EMPTY_CONSUMER, on_complete=EMPTY_ACTION,
                             on_after_terminate=EMPTY_ACTION)

    def doOnError(self, func):
        return self.doOnEach(on_next=EMPTY_CONSUMER, on_error=func, on_complete=EMPTY_ACTION,
                             on_after_terminate=EMPTY_ACTION)

    def doOnEach(self, on_next, on_error, on_complete, on_after_terminate):
        return ObservableOnEach(self, on_next, on_error, on_complete, on_after_terminate)

    def toList(self):
        return ObservableToListSingle(self)


class ObservableOnEach(Observable, ObservableSource):
    def __init__(self, source, on_next, on_error, on_complete, on_after_terminate):
        """
        
        :param ObservableSource source: 
        :param on_next: 
        :param on_error: 
        :param on_complete: 
        :param on_after_terminate: 
        """
        super(ObservableOnEach, self).__init__(source)
        self._on_next = on_next
        self._on_error = on_error
        self._on_complete = on_complete
        self._on_after_terminate = on_after_terminate

    def subscribe(self, observer):
        class DoOnEachObserver(Observer, Disposable):
            def __init__(self, actual, on_next, on_error, on_complete, on_after_terminate):
                """
                :param Observer actual: 
                :param on_next: 
                :param on_error: 
                :param on_complete: 
                :param on_after_terminate: 
                """
                self.actual = actual
                self.on_next = on_next
                self.on_error = on_error
                self.on_complete = on_complete
                self.on_after_terminate = on_after_terminate
                self.s = None

            def isDisposed(self):
                self.s.isDisposed()

            def dispose(self):
                self.s.dispose()

            def onComplete(self):
                self.on_complete()
                self.actual.onComplete()

            def onSubscribe(self, disposable):
                self.s = disposable
                self.actual.onSubscribe(self)

            def onError(self, err):
                self.on_error(err)
                self.actual.onError(err)

            def onNext(self, t):
                self.on_next(t)
                self.actual.onNext(t)

        o = DoOnEachObserver(observer, self._on_next, self._on_error, self._on_complete, self._on_after_terminate)
        self.source.subscribe(o)
        return o


class ObservableCreate(Observable):
    class CreateEmitter(ObservableEmitter, Disposable):

        def __init__(self, observer_):
            self._disposable = None
            self._observer = observer_

        def onNext(self, t):
            if not self.isDisposed():
                self._observer.onNext(t)

        def onComplete(self):
            if not self.isDisposed():
                try:
                    self._observer.onComplete()
                except:
                    self.dispose()

        def onError(self, err):
            self._observer.onError(err)

        def setDisposable(self, disposable):
            """

            :type disposable: Disposable
            """
            assert isinstance(disposable, Disposable), "must be Disposable but %s" % disposable
            if self._disposable:
                self._disposable.dispose()

            self._disposable = disposable

        def isDisposed(self):
            return self._disposable is not None and self._disposable.isDisposed()

        def dispose(self):
            if self._disposable:
                self._disposable.dispose()

            self._disposable = None

    def __init__(self, source):
        """

        :type source: ObservableOnSubscribe
        """
        assert isinstance(source, ObservableOnSubscribe), "source must be ObservableOnSubscribe but %s" % type(source)
        super(ObservableCreate, self).__init__(source)

    def subscribe(self, observer):
        assert isinstance(observer, Observer)
        parent = ObservableCreate.CreateEmitter(observer)
        observer.onSubscribe(parent)
        try:
            self.source.subscribe(parent)
            return observer
        except Exception as err:
            THROW_IF_FATAL(err)
            exc_info = sys.exc_info()
            parent.onError(exc_info)


class ObservableMap(Observable, ObservableSource):
    source = None
    func = None

    def __init__(self, source, func):
        super(ObservableMap, self).__init__(source)
        self.func = func

    def subscribe(self, observer):
        """
        :param LambdaObserver observer: 
        :return: Disposable
        """

        class MapObserver(BasicObserver):

            def __init__(self, actual, mapper):
                """

                :type mapper: callable
                :type actual: Observer
                """
                super(MapObserver, self).__init__(actual)
                self.mapper = mapper

            def onNext(self, t):
                try:
                    return self.actual.onNext(self.mapper(t))
                except Exception as err:
                    self.actual.dispose()
                    self.actual.onError(err)

        o = MapObserver(observer, self.func)
        self.source.subscribe(o)
        return o


class ObservableFlatMap(Observable, ObservableSource):
    class MergeObserver(Observer, Disposable):
        _canceled = True
        _done = False
        _error = None
        disposable = None
        _wip = 0

        def __init__(self, child, mapper, maxConcurrency, bufferSize):
            """

            :type mapper: callable
            :type child: Observer
            """
            assert isinstance(child, Observer), "child must be Observer but %s" % type(child)
            self._observer = None
            self.bufferSize = bufferSize
            self.maxConcurrency = maxConcurrency
            self.child = child
            self.mapper = mapper
            self._sources = collections.deque()

        def onSubscribe(self, disposable):
            self.disposable = disposable
            self.child.onSubscribe(self)

        def onError(self, err):
            self._error = err
            self.child.onError(err)

        def isDisposed(self):
            return self._canceled

        def onComplete(self):
            if self._done:
                return None
            self._done = True
            self.child.onComplete()

        def onNext(self, t):
            inner_source = self.mapper(t)
            assert isinstance(inner_source,
                              ObservableSource), "flatMap function result must be Observable but %s" % inner_source

            if self._wip == self.maxConcurrency:
                # TODO
                self._sources.append(inner_source)
                return None

            class InnerObserver(BasicObserver):
                def onComplete(self):
                    pass

                def onNext(self, t):
                    self.actual.onNext(t)

            o = InnerObserver(self.child)
            self._observer = o
            inner_source.subscribe(o)

        def dispose(self):
            self._canceled = True
            self.disposeAll()

        def disposeAll(self):
            self._observer.dispose()

    def __init__(self, source, mapper, maxConcurrency, bufferSize):
        """

        :type source: ObservableSource
        """
        super(ObservableFlatMap, self).__init__(source)
        self.bufferSize = bufferSize
        self.maxConcurrency = maxConcurrency
        self.mapper = mapper

    def subscribe(self, observer):
        assert isinstance(observer, Observer), "observer must be Observer type but %s" % type(observer)
        o = ObservableFlatMap.MergeObserver(observer, self.mapper, self.maxConcurrency, self.bufferSize)
        self.source.subscribe(o)
        return o.disposable


class ObservableOnSubscribe(ObservableSource):
    def __init__(self):
        self.__on_subscribe = None

    @staticmethod
    def create(on_subscribe):
        assert callable(on_subscribe), "must be a function %s" % repr(on_subscribe)
        o = ObservableOnSubscribe()
        o.__on_subscribe = on_subscribe
        return o

    def subscribe(self, observable_emitter):
        isinstance(observable_emitter, Emitter)
        self.__on_subscribe(observable_emitter)


class ObservableToListSingle(Single):
    class ToListObserver(Observer, Disposable):
        def __init__(self, actual):
            """

            :type actual: SingleObserver
            """
            self.actual = actual
            self.collection = []
            self.s = None

        def isDisposed(self):
            self.s.isDisposed()

        def dispose(self):
            self.s.dispose()

        def onComplete(self):
            self.actual.onSuccess(self.collection)

        def onSubscribe(self, disposable):
            if not self.s:
                self.s = disposable
                self.actual.onSubscribe(self)

        def onError(self, err):
            self.collection = None
            self.actual.onError(err)

        def onNext(self, t):
            self.collection.append(t)

    def __init__(self, observable_source):
        """

        :type observable_source: ObservableSource
        """
        assert isinstance(observable_source, ObservableSource), \
            "must be ObservableSource but %s" % type(observable_source)

        self.source = observable_source

    def subscribe(self, single_observer):
        """

        :type single_observer: SingleObserver
        """
        assert isinstance(single_observer, SingleObserver), \
            "`actual` must be SingleObserver type but %s" % type(single_observer)
        observer = ObservableToListSingle.ToListObserver(single_observer)
        self.source.subscribe(observer)
        return observer
