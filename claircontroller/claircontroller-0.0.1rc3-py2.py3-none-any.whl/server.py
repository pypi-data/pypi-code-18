import json
from threading import Thread, get_ident
from bottle import route, run, template, request
from queue import Queue
from kontroller import log
from .client import VulnerabilityGetupIoV1Api

q = Queue()

@route('/report/', ['GET', 'POST'])
@route('/report', ['GET', 'POST'])
def index():
    data = request.json
    notification = data['Notification']
    name = notification['Name']
    log('Notification: {}'.format(name))
    #q.put(name)

    return 'OK\n'


def api_server_worker():
    log('Started API Server thread %s at 0.0.0.0:8080' % get_ident())
    return run(host='0.0.0.0', port=8080)


def start_api_server():
    t = Thread(target=api_server_worker, daemon=True)
    t.start()
    return q
