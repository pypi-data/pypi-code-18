from .errors import *
from pebble import ProcessPool
from multiprocessing import Process, Pipe, Pool

class Task():
    def __init__(self, function, args=(), timeout=600):
        self.function = function
        self.args = args
        self.timeout = timeout

    def run(self):
        # thread = Process(target=self.function, args=self.args)
        # thread.start()
        # thread.join(self.timeout)
        # thread.get()
        # if thread.is_alive():
        #     thread.terminate()
        #     thread.join()
        #     raise TimeoOutError('Killed after %d seconds.'%self.timeout)
        with ProcessPool() as pool:
            pool.schedule(self.function, args=self.args, timeout=self.timeout)
            # result = task.get()
            # except TimeoutError:
            #     print ("Task: %s took more than 5 seconds to complete" % task)
