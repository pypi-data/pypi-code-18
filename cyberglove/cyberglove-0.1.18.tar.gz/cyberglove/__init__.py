import os
import time
import serial
from glob import glob
from os.path import dirname, join
from .cyberglove import getdata, clean, init as raw_init  # noqa

# Default config file is next to this file
TEMP_CONFIG = join(dirname(__file__), '{}.temp.config'.format(time.time()))
TEMPLATE_CONFIG = join(dirname(__file__), 'template.config')
DEFAULT_CALIB = join(dirname(__file__), 'calib', 'default.calib')
DEFAULT_HANDRANGE = join(dirname(__file__), 'calib', 'default.handRange')
DEFAULT_USERRANGE = join(dirname(__file__), 'calib', 'default.userRange')


def is_valid_port(port):
    ''' Test all of the windows COM ports and return which are openable '''
    try:
        s = serial.Serial(port, baudrate=115200, timeout=1.5)
        # Disable streaming, if currently streaming
        s.write(b'\x03')
        s.send_break(duration=0.7)
        # Request info
        s.write(b'?i')
        response = s.read(10000)
        s.close()
        return b'CyberGlove Corporation' in response
    except (OSError, serial.SerialException):
        return False


def find_port():
    ''' Try to find a cyberglove serial port '''
    if os.name == 'posix':
        ports = glob('/dev/cu.usb*') + glob('/dev/ttyACM*')
    elif os.name == 'nt':
        ports = ['COM{}'.format(i) for i in range(1, 257)]
    else:
        raise Exception('Unsupported operating system: {}'.format(os.name))

    valid_ports = [p for p in ports if is_valid_port(p)]

    if len(valid_ports) == 0:
        raise Exception('No matching serial port found for cyberglove!\n' +
                        'Is it plugged in to USB and turned on?')
    elif len(valid_ports) == 1:
        return valid_ports[0]
    else:
        raise Exception('Multiple valid ports found: {}'.format(valid_ports))


def cleanup_temp_configs():
    ''' Remove lingering temporary config files '''
    # Note: we do this because windows lacks a reusable named temporary file
    for fname in glob(join(dirname(__file__), '*.temp.config')):
        os.remove(fname)


def make_config(port=None,
                logfile="none",
                calibfile=DEFAULT_CALIB,
                userrangefile=DEFAULT_USERRANGE,
                handrangefile=DEFAULT_HANDRANGE):
    template = open(TEMPLATE_CONFIG, 'r').read()
    port = port or find_port()
    return template.format(port=port,
                           logfile=logfile,
                           calibfile=calibfile,
                           userrangefile=userrangefile,
                           handrangefile=handrangefile)


def init(config_filename=None, port=None):
    ''' Create a default config file dynamically if no filename provided '''
    if config_filename is None:
        config = make_config()
    else:
        config = open(config_filename, 'r').read()
    # Workaround the fact that windows doesn't have reusable named tempfiles
    cleanup_temp_configs()
    with open(TEMP_CONFIG, 'w') as f:
        f.write(config)
    return raw_init(TEMP_CONFIG)
