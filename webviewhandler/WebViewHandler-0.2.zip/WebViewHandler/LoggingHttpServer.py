from BaseHTTPServer import BaseHTTPRequestHandler
import os
import json
from hashlib import md5
from urlparse import urlparse, parse_qs
import time


class LoggingHttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.template = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates', 'base.html')).read()
        self.path = None
        self.params = None
        self.query = None
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def render(self, template_name, **kwargs):
        self.wfile.write(self.template)

    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data))

    def route_root(self):
        self.send_response(200)
        self.send_header("Content-type", 'text/html; charset=utf-8')
        self.end_headers()
        self.render('base.html', name='test')

    def route_getlogs(self):
        buf = self.server.buffer
        if not buf:
            time.sleep(0.5)
            return self.route_getlogs()
        tempbuffer = buf[:]
        log_text = '\n'
        if 'lastline' in self.query and self.query['lastline'][0]:
            for i in xrange(-1, -len(buf) - 1, -1):
                line_text = self.server.format(buf[i])
                line_hash = md5(line_text).hexdigest()
                if line_hash == self.query['lastline'][0]:
                    if i == -1:
                        time.sleep(0.5)
                        return self.route_getlogs()
                    tempbuffer = buf[i + 1:]
                    break
        tempbuffer = map(lambda x: self.server.format(x), tempbuffer)
        log_text += '\n'.join(tempbuffer)

        self.send_json({
            'logs': log_text,
            'last_line_hash': md5(tempbuffer[-1]).hexdigest(),
        })

    def dispatch(self):
        parse_obj = urlparse(self.path)
        self.path = parse_obj[2]
        self.params = parse_obj[3]
        self.query = parse_qs(parse_obj[4])
        func_name = 'route_' + self.path.strip('/')
        if not hasattr(self, func_name):
            self.send_response(404)
            self.send_header("Content-type", 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('Page not found')
            return
        return getattr(self, func_name)()

    def do_GET(self):
        if self.path == '/':
            return self.route_root()
        return self.dispatch()
