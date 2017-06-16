import sys
import signal
import logging
import threading

import modpy

from . import dirconfig
from .command import Command

def signal_handler(signal, frame):
    sys.exit(0)

def print_prompt():
    sys.stdout.write('MODPY> ')
    sys.stdout.flush()

def start_node(node):
    node.start()

def shell(node):
    # XXX: Wait 1 sec for node to start so that prompt is emitted last.
    # XXX: Find a better method!
    import time
    time.sleep(1)
    
    Command.init(node)
    print_prompt()
    while True:
        line = input()
        words = line.split()
        if len(words) > 0:
            Command.process(line)
        print_prompt()

def main():
    # init
    dirconfig.init()
    signal.signal(signal.SIGINT, signal_handler)

    node = modpy.init_node()
    loop = node.event_loop()

    logging.basicConfig(level=logging.DEBUG)
    loop.set_debug(True)

    try:
        modpy_thr = threading.Thread(target=start_node, args=(node, ))
        modpy_thr.start()
        
        #shell_thr = threading.Thread(target=shell, args=(node, ))
        #shell_thr.start()
        shell(node)
    except (KeyboardInterrupt, SystemExit):
        modpy.stop_node()
        sys.exit(0)
        
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
