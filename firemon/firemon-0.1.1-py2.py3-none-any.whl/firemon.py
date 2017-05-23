import psutil
import time
from firebase import firebase
from datetime import datetime
from slugify import slugify
import os
import socket

f = firebase.FirebaseApplication('https://%s.firebaseio.com' % os.getenv('FIREMON_PROJECTID'), None)
authentication = firebase.FirebaseAuthentication(os.getenv('FIREMON_DBSECRET'), os.getenv('FIREMON_USER'))
f.authentication = authentication

SERVER_NAME = os.getenv('FIREMON_NAME', socket.gethostname())

def cli():
    while True:
        du = psutil.disk_usage('/')
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        load = os.getloadavg()

        data = {
            'name': SERVER_NAME,
            'cpu': {
                'count': psutil.cpu_count(),
                'percent': psutil.cpu_percent(interval=None)
            },
            'load': {
                '0': load[0],
                '1': load[1],
                '2': load[2]
            },
            'boottime': datetime.fromtimestamp(psutil.boot_time()),
            'memory': {
                'virtual': {
                    'total': mem.total,
                    'free': mem.free,
                    'percent': mem.percent,
                    'used': mem.used,
                    'available': mem.available
                },
                'swap': {
                    'total': swap.total,
                    'free': swap.free,
                    'percent': swap.percent,
                    'used': swap.used,
                }
            },
            'disk': {
                'percent': du.percent,
                'free': du.free,
                'total': du.total,
                'used': du.used
            },
            'lastupdate': datetime.now()
        }
        result = f.put('/servers', slugify(SERVER_NAME), data)

        time.sleep(1)

if __name__ == '__main__':
    cli()
