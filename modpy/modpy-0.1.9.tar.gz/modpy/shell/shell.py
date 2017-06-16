class ShellThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        if self.is_alive() == True:
            self.stop_event.set()
            self.join()
                
