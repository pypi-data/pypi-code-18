import gevent
import random

def task(obj):
    pid=obj['pid']
    '''
    Some non-deterministic task
    '''
    gevent.sleep(random.randint(0,2)*0.1)
    print('Task %s done' % pid)

def synchronous():
    for i in range(1,10):
        task({"pid":i})

def asynchronous():
    threads = [gevent.spawn(task, {'pid':i}) for i in xrange(10)]
    gevent.joinall(threads)

print('Synchronous:')
synchronous()

print('Asynchronous:')
asynchronous()