import threading
import queue

class Routine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.sender = None

    def run(self):
        while True:
            self.queue.get()
            self.sender.send_status()
            self.queue.task_done()
