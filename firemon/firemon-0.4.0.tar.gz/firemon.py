import psutil
import time
from datetime import datetime
from slugify import slugify
import os
import socket
import requests

SERVER_NAME = os.getenv('FIREMON_NAME', socket.gethostname())
SERVER_URL = 'https://makara.io/servers/%s' % slugify(SERVER_NAME)

TIMEOUT = 1

def cli():
    network = psutil.net_io_counters()

    bytes_recv = network.bytes_recv
    bytes_sent = network.bytes_sent

    while True:
        start_time = time.time()

        du = psutil.disk_usage('/')
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        load = os.getloadavg()
        network = psutil.net_io_counters()

        data = {
            's': SERVER_NAME, # name
            'c': [ # cpu
                psutil.cpu_count(), # count
                psutil.cpu_percent(interval=None) # percent
            ],
            'l': load, # load
            'b': datetime.fromtimestamp(psutil.boot_time()).astimezone().isoformat(), # boottime
            'm': [ # memory
                [ # virtual
                    mem.total, # total
                    mem.free, # free
                    mem.percent, # percent
                    mem.used, # used
                    mem.available # a
                ],
                [
                    swap.total, # total
                    swap.free, # free
                    swap.percent, # percent
                    swap.used # used
                ]
            ],
            'd': [ # disk
                du.percent, # percent
                du.free, # free
                du.total, # total
                du.used # used
            ],
            'n': [ # network
                network.bytes_sent - bytes_sent, # bytes sent last 1 sec
                network.bytes_recv - bytes_recv, # bytes received last 1 sec
                network.bytes_sent, # bytes sent total
                network.bytes_recv # bytes received total
            ],
            'u': datetime.utcnow().isoformat() # lastupdate
        }

        bytes_sent = network.bytes_sent
        bytes_recv = network.bytes_recv

        try:
            requests.put(SERVER_URL, json=data, timeout=TIMEOUT)
            print("Request sent: %s" % datetime.now())
        except Exception as identifier:
            print("Request unsuccessful : %s" % identifier)

        if time.time() - start_time < 1:
            time.sleep(1 - (time.time() - start_time))

if __name__ == '__main__':
    cli()
