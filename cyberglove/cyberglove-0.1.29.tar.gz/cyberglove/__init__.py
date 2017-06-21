import os
import time
import logging
import serial
from glob import glob
from os.path import dirname, join
from .cyberglove import getdata, getsample, clean, init as raw_init  # noqa

# Default config file is next to this file
TEMP_CONFIG = join(dirname(__file__), '{}.temp.config'.format(time.time()))
TEMPLATE_CONFIG = join(dirname(__file__), 'template.config')
DEFAULT_CALIB = join(dirname(__file__), 'calib', 'default.calib')
DEFAULT_HANDRANGE = join(dirname(__file__), 'calib', 'default.handRange')
DEFAULT_USERRANGE = join(dirname(__file__), 'calib', 'default.userRange')

logging.basicConfig()
logger = logging.getLogger('cyberglove')
logger.setLevel(logging.DEBUG)


def get_glove_info(port):
    ''' Query cyberglove for basic info '''
    logger.info('get_glove_info({})'.format(port))
    s = serial.Serial(port, baudrate=115200, timeout=0.5)
    s.write(b'?i?i')
    return b'CyberGlove Corporation' in s.read(10000)


def stop_streaming(port):
    ''' Stop streaming date from the cyberglove '''
    logger.info('stop_streaming({})'.format(port))
    s = serial.Serial(port, baudrate=115200, timeout=0.5)
    s.write(b'\x03')
    s.flush()
    del s
    return get_glove_info(port)


def reset_glove(port):
    ''' Software reset of the cyberglove -- Takes a long time '''
    logger.info('reset_glove({})'.format(port))
    s = serial.Serial(port, baudrate=115200, timeout=20.0)
    s.write(b'\x12')
    res = b'CyberGlove Corporation' in s.read(10000)
    s.flush()
    return res


def is_valid_glove(port):
    ''' Query cyberglove status, return True if valid '''
    logger.info('is_valid_glove({})'.format(port))
    s = serial.Serial(port, baudrate=115200, timeout=0.5)
    s.write(b'?G?G')
    response = s.read(10000)  # definitely timeout
    if b'G' not in response:
        logger.debug('is_valid_glove({}): missing response echo'.format(port))
        return False
    truncated = response[response.find(b'G'):]
    if len(truncated) < 3:
        logger.debug('is_valid_glove({}): response {} too short'.format(port, truncated))
        return False
    if truncated[2] != 0:
        logger.debug('is_valid_glove({}): missing termination ({})'.format(port, truncated[2]))
        return False
    logger.info('is_valid_glove({}): got ({})'.format(port, truncated[1]))
    return bool(truncated[1])


def is_valid_port(port):
    ''' Test all of the windows COM ports and return which are openable '''
    try:
        if not get_glove_info(port):
            if not stop_streaming(port):
                if not reset_glove(port):
                    return False
        return is_valid_glove(port)
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

    logger.info('find_port(): candidate ports: {}'.format(ports))

    valid_ports = [p for p in ports if is_valid_port(p)]
    logger.info('find_port(): valid ports: {}'.format(valid_ports))

    if len(ports) == 0:
        raise Exception('No matching serial port found for cyberglove!\n' +
                        'Is it plugged in to USB and turned on?')
    elif len(valid_ports) == 1:
        return valid_ports[0]
    elif len(valid_ports) == 0 and len(ports) == 1:
        print('Serial port could not be validated, but only one matches.')
        return ports[0]
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
    logger.info('make_config(port={})'.format(port))
    template = open(TEMPLATE_CONFIG, 'r').read()
    port = port or find_port()
    logger.info('make_config(): using port: {}'.format(port))
    return template.format(port=port,
                           logfile=logfile,
                           calibfile=calibfile,
                           userrangefile=userrangefile,
                           handrangefile=handrangefile)


def init(config_filename=None, port=None):
    ''' Create a default config file dynamically if no filename provided '''
    logger.info('init(config_filename={}, port={})'.format(config_filename, port))
    if config_filename is None:
        config = make_config()
    else:
        config = open(config_filename, 'r').read()
    # Workaround the fact that windows doesn't have reusable named tempfiles
    cleanup_temp_configs()
    with open(TEMP_CONFIG, 'w') as f:
        f.write(config)
    return raw_init(TEMP_CONFIG)
