import re
import glob
import struct
from serial import Serial
import serial
from multiprocessing import Array, Lock, Queue, queues
from multiprocessing import Process
import time
import atexit
import signal
import os
import numpy as np


def find_port():
    '''
    Heuristics for finding what serial port a cyberglove is on.
    '''
    results = []
    while len(results) == 0:
        results = glob.glob('/dev/cu.usbserial-A*')
        if len(results) == 0:
            print("Cannot find cyberglove. Plug the cable. Sleeping.")
            time.sleep(3)
    if len(results) > 1:
        print("WARNING: more than one cyberglove found, using first")
    return Serial(results[0],
                  timeout=None,
                  write_timeout=None,
                  inter_byte_timeout=None,
                  baudrate=115200,
                  bytesize=serial.EIGHTBITS,
                  stopbits=serial.STOPBITS_ONE,
                  parity=serial.PARITY_NONE,
                  exclusive=True)

class CyberGlove():
    _time_regex = b'..:..:..:..:.S'
    _packet = '>xxxxxxxxxxxxxxHHHHHHHHHHHHHHHHHHHHHHxxx'  # packet byte structure
    _packet_len = struct.calcsize(_packet)

    def __init__(self):
        print("Initializing cyberglove.")
        self._shared_data = Array("i", [0] * 22)
        self._lock = Lock()
        self._queue = Queue(maxsize=1)
        self._process = Process(target=self._reader, args=(self._shared_data, self._lock, self._queue))
        self._process.daemon = True
        self._process.start()

    def read(self):
        self._queue.get()
        with self._lock:
            return self._shared_data[:]

    def _reader(self, shared_data, lock, queue):
        self._last_resync = 0
        # Resets port so it's clean.
        port = find_port()
        port.write(b'\x03')
        port.flush()
        port.reset_input_buffer()
        port.reset_output_buffer()
        port.close()
        self._port = find_port()

        atexit.register(self._close_port)
        signal.signal(signal.SIGINT, self._close_port)
        signal.signal(signal.SIGTERM, self._close_port)
        self._port.write(b'1E4010111\0')
        self._port.flush()
        self._port.write(b'1S\0')
        self._port.flush()
        while True:
            try:
                data = self._port.read(self._packet_len)
            except OSError:
                return
            if not re.match(self._time_regex, data):
                data = self._sync()
            packet = struct.unpack(self._packet, data)
            with lock:
                shared_data[:] = packet[:]
            try:
                queue.put(True, block=False)
            except queues.Full:
                pass

    def _sync(self):
        ''' Recover an out-of-sync stream, returning a packet after sync '''
        find = None
        while find is None:
            print('Re-synching data stream')
            if time.time() - self._last_resync < 1:
                print("Re-syncing occurred twice within a sec.")
                print("Unplug and plug your cyberglove. Quitting.")
                os.kill(os.getppid(), signal.SIGKILL)
                exit(-1)
            self._last_resync = time.time()
            data = self._port.read(2 * self._packet_len)
            find = re.search(self._time_regex, data)
        self._port.read(find.start())  # Dump remainder bytes
        return self._port.read(self._packet_len)  # return next packet

    def _close_port(self, *args, **kwargs):
        # Active waiting for process to finish.
        if hasattr(self, "_port") and self._port.is_open:
            self._port.write(b'\x03')
            self._port.flush()
            self._port.close()


if __name__ == '__main__':
    cg = CyberGlove()
    cg.read()
    count = 0
    start = time.time()
    max_val = np.array(cg.read())
    min_val = np.array(cg.read())
    while True:
        data = cg.read()
        print("data: %s" % data)
        max_val = np.maximum(np.array(data), max_val)
        min_val = np.minimum(np.array(data), min_val)
        print("max : %s" % max_val.tolist())
        print("min : %s" % min_val.tolist())
        count += 1
        print("times per sec: %f" % (count / (time.time() - start)))
        print("")
