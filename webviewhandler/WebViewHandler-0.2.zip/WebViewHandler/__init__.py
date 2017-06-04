import logging.handlers
from .LoggingHttpServer import LoggingHttpRequestHandler
import SocketServer
import threading
import logging


class WebViewHandler(logging.handlers.BufferingHandler):
    def __init__(self, host='0.0.0.0', port=8080, capacity=1000, run=True):
        '''
        Rotating logging handler that stores log entries in memory and serves
        the logs to a web client.
        :param host: Host IP to listen.  Default is all IPs
        :param port: Port to listen on.  Default is port 8080
        :param capacity: Number of log lines to keep, discarding the oldest as necessary
        :param run: Boolean, if true start the web server on init.
                    If false, you must call the run() function to start the server.
        '''
        self.port = port
        self.host = host
        super(WebViewHandler, self).__init__(capacity=capacity)
        if run:
            self.run()

    def flush(self):
        self.acquire()
        try:
            while self.shouldFlush(None):
                self.buffer.pop(0)
        finally:
            self.release()

    def format(self, record):
        if self.formatter:
            return super(WebViewHandler, self).format(record)
        else:
            return logging.Formatter('%(asctime)s %(message)s').format(record)

    def run(self):
        httpd = SocketServer.ThreadingTCPServer((self.host, self.port), LoggingHttpRequestHandler)
        httpd.daemon_threads = True
        httpd.buffer = self.buffer
        httpd.format = self.format
        t = threading.Thread(target=httpd.serve_forever)
        t.daemon = True
        t.start()
