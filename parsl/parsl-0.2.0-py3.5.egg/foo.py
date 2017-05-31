import atexit
import time

from ipyparallel.apps import ipcontrollerapp as app
app.launch_new_instance()
time.sleep(30)
