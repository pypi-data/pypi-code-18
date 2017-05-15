# clock.py
#
#

""" timer, repeater and other clock based classes. """

from .event import Event
from .object import Default, Config, Object
from .utils import day, elapsed, get_day, get_hour, now, to_day, to_time
from .utils import name, sname
from .error import ENODATE
from .space import cfg

import threading
import logging
import time
import os

start = 0

class Timer(Object):

    """
        call a function as x seconds of sleep.

    """

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__(**kwargs)
        self._state = Default(default="")
        self._counter = Default(default=0)
        self._time = Default(default=0)
        self._time.start = time.time()
        self._time.latest = time.time()
        self._state.status = "waiting"
        self._name = kwargs.get("name", name(func))
        self.sleep = sleep
        self.func = func
        self.args = args
        try:
            self._event = self.args[0]
            self._state.origin = self._event.origin
        except:
            self._event = Event()
        self.kwargs = kwargs

    def start(self):
        """ start the timer. """
        timer = threading.Timer(self.sleep, self.run)
        timer.setDaemon(True)
        timer.setName(self._name)
        timer.sleep = self.sleep
        timer._state = self._state
        timer._name = self._name
        timer._time = self._time
        timer._counter = self._counter
        self._counter.run += 1
        self._time.latest = time.time()
        timer.start()
        return timer

    def run(self, *args, **kwargs):
        """ run the registered function. """
        self._time.latest = time.time()
        self.func(*self.args, **self.kwargs)
 
    def exit(self):
        """ cancel the timer. """
        self._status = ""
        self.cancel()

class Repeater(Timer):

    """
        Repeat an funcion every x seconds. 

        >>> def func(event): event.reply("yo!")

        >>> from bot.clock import Repeater
        >>> from bot.time import now
        >>> repeater = Repeater(now(), func)
        >>> repeater.start()[B

    """
    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__(sleep, func, *args, **kwargs) 
        logging.warn("# start %s" % kwargs.get(name, sname(func)))

    def run(self, *args, **kwargs):
        self._time.start = time.time()
        self._time.run += 1
        try:
            self.func(*self.args, **self.kwargs)
        except:
            logging.error(get_exception())
        self.start()

def init(event):
    from .space import cfg, db, kernel
    cfg = Config(default=0).load(os.path.join(cfg.workdir, "runtime", "timer"))
    cfg.template("timer")
    timers = []
    for e in db.sequence("timer", cfg.latest):
        if e.done: continue
        if "time" not in e: continue
        if time.time() < int(e.time):
            timer = Timer(int(e.time), e.direct, e.txt)
            t = kernel.launch(timer.start)
            timers.append(t)
        else:
            cfg.last = int(e.time)
            cfg.save()
            e.done = True
            e.sync()
    return timers
