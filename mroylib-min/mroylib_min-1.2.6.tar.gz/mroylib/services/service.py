from queue import Queue, Empty
from functools import partial
from copy import  deepcopy
import ctypes
from concurrent.futures import  ThreadPoolExecutor, ProcessPoolExecutor
from qlib.log import show
from functools import partial
# import asyncio
import grequests as async

err_log = partial(show, color='red', a=['underline'])

def thread_patch(fun,pargs, num=7, type='thread'):
    args = []
    for ar in pargs:
        if isinstance(ar, (tuple,list, )):
            args.append(ar)

        elif isinstance(ar, (str, int,)):
            args.append((ar,))
        else:
            args.append((ar,))

    with ThreadPoolExecutor(num) as exe:
        m = [exe.submit(fun, *arg) for arg in args]
        for i in m:
            yield i.result()


def net_patch(urls, err_handler=err_log, callback=None, **kargs):
    """
    @fun only:
        def xxxfun(response):
            ....
            return result
    """
    result = {}

    def patch_result(response, *args, **kargs):
        res = callback(response)
        url = response.url
        show(response.url, response.status_code, log=True, k='debug')
        result[url] = res
    if callback:
        ars = (async.get(u,hooks={'response': [patch_result]}, **kargs) for u in urls)
    else:
        ars = (async.get(u, **kargs) for u in urls)
    _res = async.map(ars, exception_handler=err_handler)
    if not callback:
        return _res
    return result





class LinkError(Exception):
    pass

class MissionPassError(TypeError):
    pass

class Links:

    def __init__(self, funs, *args, to=None, thread=False, process=False, io=False, net=False, **kargs):
        self.to = to
        self.thread = thread
        self.io = io
        self.process = process
        self.net = net
        self.funs = self.funs
        self.args = args
        self.kargs = kargs

    def link_test(self):
        funs = deepcopy(self.funs)
        last_res = ()
        while funs:
            f = funs.pop()

            res = f(*self.args, **self.kargs)

    def __call__(self):
        if self.to:
            res = self.fun()
            if isinstance(res, tuple):
                pass
            else:
                pass





class Pid:
    _funs = set()
    _links = set()

    def __init__(self):
        pass

    def push(self, fn):
        fn = fn
        Pid.push(fn)