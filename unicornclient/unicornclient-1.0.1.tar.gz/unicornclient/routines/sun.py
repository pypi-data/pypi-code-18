import threading
import Queue

class Routine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = Queue.Queue()

    def run(self):
        while True:
            self.queue.get()
            self.queue.task_done()
