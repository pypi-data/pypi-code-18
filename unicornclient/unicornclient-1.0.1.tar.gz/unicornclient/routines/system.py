import threading
import Queue
import subprocess

class Routine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.authorized_commands = ['reboot', 'halt']

    def run(self):
        while True:
            data = self.queue.get()
            command = data['command'] if 'command' in data else None

            if command in self.authorized_commands:
                subprocess.call(command, shell=True)

            self.queue.task_done()
