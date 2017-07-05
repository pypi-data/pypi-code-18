import logging
import multiprocessing
import sys
import time
from unittest import TestCase

import rexpython as rx

logging.basicConfig(format="%(asctime)-15s %(name)-25s %(levelname)s %(process)d %(message)s")

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class TestObservable(TestCase):
    def test_blockingSubscribe(self):
        d = rx.Observable.from_(xrange(1, 4)).blockingSubscribe(
            on_next=lambda i: sys.stdout.write("from=%s\n" % i),
            on_complete=lambda: sys.stdout.write("!! complete\n")
        )

        print d

    def test_play(self):
        def ga(i):
            while True:
                log.debug("ga %s" % i)
                time.sleep(1)

        plist = []
        for i in xrange(1, 5):
            p = multiprocessing.Process(target=ga, args=(i,))
            p.start()

            plist.append(p)

        for pp in plist:
            print pp
            pp.join()

        print "PLAY"

    def test_observeOn(self):
        def emit(emitter):
            """

            :type emitter: rx.ObservableEmitter
            """

            emitter.setDisposable(rx.ActionDisposable(lambda: sys.stdout.write("disposed")))
            for i in xrange(1, 30):
                log.debug("emit %s" % i)
                emitter.onNext(i)
                time.sleep(1)
            emitter.onComplete()

        log.info("hello")
        log.debug("main process is %s\n" % multiprocessing.current_process().pid)
        o = rx.Observable.create(emit).observeOn(multiprocessing.Process)
        d = o \
            .doOnNext(lambda x: log.debug("doonnext=%s" % x)).map(lambda x: x * 10) \
            .blockingSubscribe(on_next=lambda x: log.debug("subscribe x=%s" % x),
                               on_error=lambda e: log.error("onerror!!!!1111111"))

        print "d=", d


def test_subscribeOn(self):
    def emit(emitter):
        """

        :type emitter: rexpython.Emitter
        """
        for i in xrange(1, 40):
            log.debug("emit %s" % i)
            emitter.onNext(i)
            time.sleep(1)

    o = rx.Observable.create(emit).doOnNext(lambda x: log.debug("doonnext=%s" % x))
    d = o.subscribeOn(multiprocessing.Process).subscribe(
        rx.LambdaObserver(on_next=lambda x: log.debug("subscribe x=%s" % x)))
    print "d=", d
