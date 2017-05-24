import psutil
import time
from datetime import datetime
from slugify import slugify
import os
import socket
import requests

SERVER_NAME = os.getenv('FIREMON_NAME', socket.gethostname())
SERVER_URL = 'http://makara.io/servers/%s' % slugify(SERVER_NAME)

requests.put(SERVER_URL, json = {})

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
            'boottime': str(datetime.fromtimestamp(psutil.boot_time())),
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
            'lastupdate': str(datetime.now())
        }

        r = requests.put(SERVER_URL, json = data)

        time.sleep(1)

if __name__ == '__main__':
    cli()
