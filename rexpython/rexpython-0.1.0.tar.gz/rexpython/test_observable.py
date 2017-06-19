import sys
import time

from rex import Observable, LambdaObserver, ActionDisposable, Disposable

if __name__ == '__main__':
    Observable.from_(xrange(1, 4)).subscribe(LambdaObserver(
        on_next=lambda i: sys.stdout.write("from=%s\n" % i),
        on_complete=lambda: sys.stdout.write("!! complete\n")
    ))

    print "-" * 120
    print "-flatMap"
    Observable.from_(xrange(1, 4)) \
        .map(lambda x: x + 1) \
        .flatMap(lambda x: Observable.from_([0, x, x * 10])) \
        .subscribe(LambdaObserver(
        on_next=lambda i: sys.stdout.write("from=%s\n" % i),
        on_complete=lambda: sys.stdout.write("!! complete\n")
    ))

    print "-" * 120
    print "-doOnNext"
    Observable.from_(xrange(1, 4)) \
        .map(lambda x: x + 1) \
        .flatMap(lambda x: Observable.from_([0, x])) \
        .doOnNext(lambda x: sys.stdout.write("do_on_next %s\n" % x)) \
        .subscribe(LambdaObserver(on_next=lambda i: sys.stdout.write("from=%s\n" % i),
                                  on_complete=lambda: sys.stdout.write("!! complete\n")
                                  ))

    print "-" * 120
    print "-doOnNext"
    Observable.from_(xrange(1, 4)) \
        .map(lambda x: x + 1) \
        .flatMap(lambda x: Observable.from_([0, x])) \
        .doOnNext(lambda x: sys.stdout.write("do_on_next %s\n" % x)) \
        .subscribe(LambdaObserver(on_next=lambda i: sys.stdout.write("from=%s\n" % i),
                                  on_complete=lambda: sys.stdout.write("!! complete\n")
                                  ))

    print "-" * 120


    def subscribe(emitter):
        emitter.setDisposable(ActionDisposable(lambda: sys.stdout.write("disposed")))

        print ("subscribed")
        for i in xrange(1, 3):
            emitter.onNext(i)
            time.sleep(1)

        # emitter.onError(Exception("foo"))
        emitter.onComplete()


    o = Observable.create(subscribe)
    o = o.map(lambda x: [x * 10, x * 100])
    o = o.flatMap(lambda x: Observable.from_(x))
    o = o.doOnNext(lambda t: sys.stdout.write("onNext%s\n" % t))
    d = o.subscribe(
        LambdaObserver(on_next=lambda i: sys.stdout.write("%s\n" % i),
                       on_complete=lambda: sys.stdout.write("complete!"),
                       on_dispose=lambda: sys.stdout.write("disposed!")))

    isinstance(d, Disposable)
    d.dispose()
