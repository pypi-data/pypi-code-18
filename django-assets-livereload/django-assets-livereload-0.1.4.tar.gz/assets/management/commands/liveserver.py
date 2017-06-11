from gevent import monkey; monkey.patch_all(thread=False)

import gevent
import gevent.queue
from gevent.lock import BoundedSemaphore
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
import json
import logging
import os
import signal
import socket
import sys
from urllib.parse import urlparse

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.utils.module_loading import import_string

from ... import bottle
from ... import watcher


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

logger = logging.getLogger(__name__)

class MessageBroker:
    def __init__(self):
        self.q_lock = BoundedSemaphore(1)
        self.queues = []

    def sub(self, queue):
        self.q_lock.acquire()
        self.queues.append(queue)
        self.q_lock.release()

    def unsub(self, queue, exit_on_empty=None):
        self.q_lock.acquire()
        self.queues.remove(queue)
        self.q_lock.release()
        if exit_on_empty is not None:
            if len(self.queues) == 0:
                exit(exit_on_empty)

    def pub(self, message):
        self.q_lock.acquire()
        queues = [q for q in self.queues]
        self.q_lock.release()
        logger.info("Sending message '"+str(message)+"' to "+str(len(queues))+" client(s).")
        for q in queues:
            q.put(message)

def reloader_loop():
    while True:
        args = [sys.executable] + ['-W%s' % o for o in sys.warnoptions] + sys.argv
        if sys.platform == "win32":
            args = ['"%s"' % arg for arg in args]
        new_environ = os.environ.copy()
        new_environ["_RUN_WSGI_SERVER"] = 'true'
        exit_code = os.spawnve(os.P_WAIT, sys.executable, args, new_environ)
        if exit_code != 3:
            return exit_code

IP_ANY = '0.0.0.0'
EXIT_AND_RELOAD = 3

class ReloadingServer:
    PID_NAME = 'livereload.pid'

    def __init__(self, ip=IP_ANY, port=8080):
        self.static_url = urlparse(settings.STATIC_URL)
        self.media_url = urlparse(settings.MEDIA_URL)

        if self.static_url.hostname:
            self._static_ip = socket.gethostbyname(self.static_url.hostname)
        else:
            self._static_ip = IP_ANY

        if self.static_url.port:
            self._static_port = self.static_url.port
        else:
            self._static_port = port

        self._django_ip = ip
        self._django_port = port

        if (self._static_ip == IP_ANY or
            self._django_ip == IP_ANY or
            self._static_ip == self._django_ip) and (self._static_port == self._django_port):
            self._separate_static_server = False
        else:
            self._separate_static_server = True

        if '_RUN_WORKER' in os.environ:
            self._type = 'worker'
        else:
            self._type = 'supervisor'

        self._django_wsgi_app = self.get_django_app()


    @classmethod
    def signal_supervisor(cls, sig_num):
        pid_path = cls.pid_path()
        if os.path.exists(pid_path):
            with open(pid_path,'r', encoding='utf-8') as pid_file:
                try:
                    server_pid = int(pid_file.read())
                    os.kill(server_pid, sig_num)
                    return True
                except:
                    pass
        return False

    @classmethod
    def get_django_app(cls):
        app_path = getattr(settings, 'WSGI_APPLICATION')
        if app_path is None:
            return get_wsgi_application()
        else:
            return import_string(app_path)


    @classmethod
    def pid_path(cls):
        # FIXME: Eventually figure out how to get the path of the main app.py
        #        so that the pid file is created there.
        return cls.PID_NAME


    def save_pid(self):
        pid = str(os.getpid())
        pid_path = self.pid_path()
        with open(pid_path,'w',encoding='utf-8') as pid_file:
            logger.info("Writing PID " + pid + " to " + pid_path)
            pid_file.write(pid)


    def start(self, pidfile=None):
        if self._type == 'supervisor':
            logger.info("Supervisor starting")
            killed_old = self.signal_supervisor(signal.SIGKILL)
            if killed_old:
                logger.info("Killed previously running supervisor")
            self.save_pid()

            def sig_handler(sig_num, stack_frame):
                if self._worker_pid:
                    logger.info("Forwaring signal "+str(sig_num)+" to worker.")
                    try:
                        os.kill(self._worker_pid, sig_num)
                    except Exception as ex:
                        logger.warn("Exception signalling worker:"+str(ex))

            signal.signal(signal.SIGUSR1, sig_handler)
            signal.signal(signal.SIGHUP, sig_handler)

            while True:
                self._worker_pid = self.spawn_worker()
                pid, exit_code = os.waitpid(self._worker_pid, options=0)
                if not os.WEXITSTATUS(exit_code) == EXIT_AND_RELOAD:
                    logger.info("Worker ({pid}) died unexpectedly with exit code {ec}, aborting.".format(ec=exit_code,pid=pid))
                    exit(exit_code)
                else:
                    logger.info("Worker exited because it needs restarting.")
        else:
            logger.info("Worker starting")
            django_server, static_server = self.create_wsgi()
            if static_server is not None:
                static_server_thread = gevent.spawn(static_server.serve_forever)
            django_server.serve_forever()

    def spawn_worker(self):
        logger.info("Spawning worker")
        args = [sys.executable] + ['-W%s' % o for o in sys.warnoptions] + sys.argv
        if sys.platform == "win32":
            args = ['"%s"' % arg for arg in args]
        new_environ = os.environ.copy()
        new_environ["_RUN_WORKER"] = 'true'
        return os.spawnve(os.P_NOWAIT, sys.executable, args, new_environ)

    def create_wsgi(self):
        app = bottle.Bottle()
        broker = MessageBroker()

        def watcher_thread():
            w = watcher.Watcher()
            for path, file_type in w.changes():
                if path is not None:
                    if file_type == watcher.Watcher.STATIC:
                        broker.pub({'action':'send', 'path':path})
                    else:
                        logger.info("Restarting because {f} changed.".format(f=path))
                        broker.pub({'action':'restart'})

        def sig_handler(sig_num, stack_frame):
            if sig_num == signal.SIGUSR1:
                logger.info("Received SIGUSR1 forcing client reload.")
                broker.pub({'action':'send','path':''})
            elif sig_num == signal.SIGHUP:
                logger.info("Received SIGHUP forcing server reload.")
                broker.pub({'action':'restart'})

        signal.signal(signal.SIGUSR1, sig_handler)
        signal.signal(signal.SIGHUP, sig_handler)

        # Add CORS headers
        @app.hook('after_request')
        def enable_cors():
            """
            You need to add some headers to each request.
            Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
            """
            bottle.response.headers['Access-Control-Allow-Origin'] = '*'
            bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
            bottle.response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        # Serve static files
        @app.route(self.static_url.path+'<filename:path>')
        def send_static(filename):
            return bottle.static_file(filename, root=settings.STATIC_ROOT)

        # Serve user-uploaded media files
        @app.route(self.media_url.path+'<filename:path>')
        def send_static(filename):
            return bottle.static_file(filename, root=settings.MEDIA_ROOT)

        @app.route(self.static_url.path+'_livereload')
        def handle_websocket():
            logger.info("Registering client")
            q = gevent.queue.Queue()
            broker.sub(q)
            exit_on_empty = None
            try:
                wsock = bottle.request.environ.get('wsgi.websocket')
                while True:
                    message = q.get()
                    if message['action'] == 'restart':
                        wsock.send(json.dumps({'reload':'', 'delay':3000}))
                        exit_on_empty = 3
                        break
                    elif message['action'] == 'send':
                        wsock.send(json.dumps({'reload':message['path'],'delay':0}))
            except WebSocketError:
                pass
            finally:
                broker.unsub(q, exit_on_empty = exit_on_empty)


        logger.info("Staring watcher thread")
        wt = gevent.spawn(watcher_thread)
        if self._separate_static_server:
            static_server = WSGIServer((self._static_ip, self._static_port), app, handler_class=WebSocketHandler)
            django_server = WSGIServer((self._django_ip, self._django_port), self.get_django_app())
        else:
            from bottle import error, request, response
            djapp = self.get_django_app()
            @error(404)
            def error404(error):
                def start_response(status, headerlist):
                    response.status = int(status.split()[0])
                    for key, value in headerlist:
                        response.add_header(key, value)
                return djapp(request.environ, start_response)
            static_server = None
            django_server = WSGIServer((self._django_ip, self._django_port), app, handler_class=WebSocketHandler)

        return django_server, static_server




class Command(BaseCommand):
    help = 'Serve static files using a CORS-enabled http.server'

    def handle(self, *args, **options):
        server = ReloadingServer()
        server.start()





