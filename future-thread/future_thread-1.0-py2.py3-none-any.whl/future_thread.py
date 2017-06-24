import sys
import logging
import threading
from concurrent import futures
from concurrent.futures._base import RUNNING, FINISHED, CANCELLED, CANCELLED_AND_NOTIFIED


class DeferredFuture(futures.Future):
    """
    Creates a thread with Future attributes.

    This simplifies starting a function in a new background thread without the overhead of using
    a ThreadPoolExecutor to provide a Future style handle around said thread.
    """
    def __init__(self, fn, *args, **kwargs):
        super(DeferredFuture, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.name = str(fn)

    def start(self):
        with self._condition:
            if self.running() or not self.set_running_or_notify_cancel():
                return

            t = threading.Thread(target=self._worker, name=self.name)
            t.daemon = True
            t.start()

    def _worker(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except BaseException:
            logging.getLogger(self.name).exception("Exception in background Future")
            e, tb = sys.exc_info()[1:]
            self.set_exception_info(e, tb)
        else:
            self.set_result(result)

    def cancel(self):
        """Cancel the future if possible.

        Returns True if the future was cancelled, False otherwise. A future
        cannot be cancelled if it has already completed.
        """
        with self._condition:
            if self._state in [FINISHED]:
                return False

            if self._state in [CANCELLED, CANCELLED_AND_NOTIFIED]:
                return True

            self._state = CANCELLED
            self._condition.notify_all()

        self._invoke_callbacks()
        return True



class Future(DeferredFuture):
    """
    Configures and immediately starts thread with Future attributes.
    """
    def __init__(self, fn, *args, **kwargs):
        super(Future, self).__init__(fn, *args, **kwargs)
        self.start()