import weresync.device as device
import weresync.interface as interface
import weresync.gui as gui
import logging
from importlib import reload

interface.start_logging_handler(stream_level=logging.DEBUG)

def setup():
    reload(device)
    reload(interface)
    reload(gui)
    global source
    global target
    global copier
    source = device.LVMDeviceManager("ubuntu-vg")
    target = device.LVMDeviceManager("ubuntu_copy_test")
    copier = device.DeviceCopier(source, target)
