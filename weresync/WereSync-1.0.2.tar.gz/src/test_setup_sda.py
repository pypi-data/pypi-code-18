import weresync.device as device
import weresync.interface as interface
import weresync.gui as gui
import weresync.plugins as plugins
import logging
from importlib import reload

interface.start_logging_handler(stream_level=logging.DEBUG)

def setup():
    reload(device)
    reload(interface)
    reload(gui)
    reload(plugins)
    global source
    global target
    global copier
    source = device.DeviceManager("/dev/sda")
    target = device.DeviceManager("/dev/sdb")
    copier = device.DeviceCopier(source, target)
