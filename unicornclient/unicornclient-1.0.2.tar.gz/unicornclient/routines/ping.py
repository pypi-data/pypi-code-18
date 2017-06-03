import threading
import Queue

class Routine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.last_ping_id = None

    def run(self):
        while True:
            data = self.queue.get()

            ping_id = data['id'] if 'id' in data else None
            if ping_id:
                self.last_ping_id = ping_id
                self.sender.send({'type': 'pong', 'id': ping_id})

            self.queue.task_done()
