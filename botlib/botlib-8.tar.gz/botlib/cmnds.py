# botlib/cmnds.py
#
#

""" botlib basic commands. """

from .object import Config, Object
from .space import runtime, users
from .space import kernel as _kernel
from .space import fleet as _fleet
from .utils import day, elapsed, get_day, get_hour, now, to_date, to_day, to_time
from .utils import name, sname, tname
from .compose import compose
from .error import ENODATE
from .clock import Timer
from .db import Db
from .trace import get_exception

import botlib.space
import threading
import _thread
import logging
import mailbox
import time
import json
import os

format = "%-4s %-18s %-8s %-8s %-15s %-15s"
starttime = time.time()

class Email(Object):
    """ Email object. """
    pass

class Entry(Object):
    """ Data Entry class . """
    pass

class Log(Entry):
    """ a log entry to log what is happening on the day. """
    pass


class Rss(Entry):
    """ a RSS entry """
    pass

class Shop(Entry):
    """ a shopping item for the wife to shop. """
    pass

class Todo(Entry):
    """ a todo entry """
    pass

class Tomorrow(Entry):
    """ a todo for tomorrow to be done. """
    pass

class Watch(Entry):
    """ files to watch. """
    pass

def alias(event):
    """ key, value alias. """
    try:
        cmnd, value = event._parsed.rest.split(" ", 1)
    except ValueError:
        event.reply('alias <cmnd> <aliased>')
        return
    if value not in _kernel._names:
        event.reply("only commands can be aliased.")
        return
    botlib.space.alias[cmnd] = value
    botlib.space.alias.save()
    event.ok(cmnd)

def announce(event):
    """ announce text on all channels in fleet. """
    _kernel.announce(event._parsed.rest)

def begin(event):
    """ begin stopwatch. """
    global starttime
    try:
        starttime = to_time(now())
    except ENODATE:
        event.reply("can't detect date from %s" % event.txt)
        return
    event.reply("time is %s" % time.ctime(starttime))

def cfg(event):
    if not users.allowed(event.origin, "OPER"):
        event.reply("you are not allowed to give the cfg command.")
        return
    args = event._parsed.args
    if not args:
        event.reply(botlib.space.cfg)
        return
    name = args[0]
    object = Config()
    object.fromdisk(name)
    try:
        key = args[1]
    except IndexError:
        event.reply(object)
        return
    if len(args) > 3:
        val = args[2:]
    elif len(args) == 3:
        val = args[2]
    else:
        event.reply("missing a value.")
        return
    try:
        object[key] = json.loads('"%s"' % val)
    except (SyntaxError, ValueError) as ex:
        event.reply(str(ex))
        return
    if key == "user" and "@" in object[key]:
        object["username"], object["server"] = object[key].split("@")
    object.sync()
    event.reply(object)

def cmnds(event):
    """ show list of commands. """
    res = sorted(set([cmnd for cmnd, mod in _kernel._names.items() if event._parsed.rest in str(mod)]))
    event.reply(res or "no modules loaded.")

def deleted(event):
    """ show deleted records. """
    event.nodel = True
    nr = 0
    db = Db()
    for object in db.selected(event):
        nr += 1
        event.display(object, event._parsed.args, str(nr))
    if not nr:
        event.reply("no results")

def dump(event):
    """ dump objects matching the given criteria. """
    nr = 0
    db = Db()
    for object in db.selected(event):
        nr += 1
        event.reply(object.nice())
    if not nr:
        event.reply("no results")

def end(event):
    """ stop stopwatch. """
    diff = time.time() - starttime
    if diff:
        event.reply("time elapsed is %s" % elapsed(diff))

def exit(event):
    """ stop the bot. """
    if not users.allowed(event.origin, "OPER"):
        event.reply("you are not allowed to give the exit command. ")
        return
    _thread.interrupt_main()

def fetcher(event):
    """ fetch all rss feeds. """
    clients = runtime.get("RSS", [])
    for client in clients:
        c = compose(client)
        thrs = c.fetcher()
        res = _kernel.waiter(thrs)
        event.reply("fetched %s" % ",".join([str(x) for x in res]))

def fleet(event):
    nr = 0
    for obj in _fleet:
        event.reply(format % (nr, obj.id(), obj._state.printable(nokeys=True), "", obj._counter.printable(), obj._error.printable(nokeys=True)))
        nr += 1
 
def find(event):
    """ present a list of objects based on prompt input. """
    nr = 0
    db = Db()
    for object in db.selected(event):
        event.display(object, event._parsed.args, str(nr), direct=True)
        nr += 1
    if not nr:
        event.reply("no results")

def first(event):
    """ show the first record matching the given criteria. """
    db = Db()
    object = db.first(*event._parsed.args)
    if object:
        event.reply(object.nice())
    else:
        event.reply("no result")

def kernel(event):
    k = _kernel
    uptime = elapsed(int(time.time() - k._time.start))
    event.reply(format % (0, "kernel", k._state.printable(nokeys=True), uptime, k._counter.printable(), k._error.printable()))

def last(event):
    """ show last objectect matching the criteria. """
    if not event._parsed.args:
        event.reply("last <prefix> <value>")
        return
    db = Db()
    object = db.last(*event._parsed.args)
    if object:
        event.reply(object.nice())
    else:
        event.reply("no result")

def log(event):
    """ log some text. """
    if not event._parsed.rest:
        event.reply("log <item>")
        return
    o = Log()
    o.log = event._parsed.rest
    o.save()   
    event.ok(1)

def loglevel(event):
    """ set loglevel. """
    from botlib.log import loglevel as _loglevel
    level = event._parsed.rest
    if not level:
        event.reply(botlib.space.cfg.loglevel)
        return
    botlib.space.loglevel = level
    _kernel.sync(os.path.join(botlib.space.cfg.workdir, "runtime", "kernel"))
    _loglevel(level)

def loud(event):
    """ disable silent mode of a bot. """
    for bot in _fleet:
        if event.id() == bot.id():
            bot.cfg.silent = False
            bot.cfg.sync() 
            event.reply("silent mode disabled.")

def license(event):
    from botlib import __license__
    event.reply(__license__)

def ls(event):
    """ show subdirs in working directory. """
    event.reply(" ".join(os.listdir(botlib.space.cfg.workdir)))

def mbox(event):
    if not event._parsed.rest:
        event.reply("mbox <path>")
        return
    fn = os.path.expanduser(event._parsed.args[0])
    event.reply("reading from %s" % fn)
    nr = 0
    if os.path.isdir(fn):
        thing = mailbox.Maildir(fn, create=False)
    elif os.path.isfile(fn):
        thing = mailbox.mbox(fn, create=False)
    else:
        event.reply("need a mbox or maildir.")
        return
    try:
        thing.lock()
    except FileNotFoundError:
        pass
    for m in thing:
        try:
            o = Email()
            o.update(m.items())
            try:
                sdate = os.sep.join(to_date(o.Date).split())
            except AttributeError:
                sdate = None
            o.text = ""
            for load in m.walk():
                if load.get_content_type() == 'text/plain':
                    o.text += load.get_payload()
            o.text = o.text.replace("\\n", "\n")
            if sdate:
                o.save(stime=sdate)
            else:
                o.save()
            nr += 1
        except:
            logging.error(get_exception())
    if nr:
        event.ok(nr)

def pid(event):
    """ show pid of the BOTLIB bot. """
    event.reply(str(os.getpid()))

def ps(event):
    """ show running threads. """
    res = []
    nr = 1
    txt = []
    k = _kernel
    for thr in sorted(k.running(), key=lambda x: tname(x)):
        object = Object(vars(thr))
        if "start" not in object._time:
            continue
        if "sleep" in object:
            uptime = elapsed(object.sleep - int(time.time() - object._time.latest))
        else:
            uptime = elapsed(int(time.time() - object._time.start))
        thrname = tname(thr)
        res = format % (nr, thrname, object._state.printable(nokeys=True), uptime, object._counter.printable(), object._error.printable(nokeys=True))
        event.reply(res.rstrip())
        nr += 1

def real_reboot():
    """ actual reboot. """
    from botlib.utils import reset
    _kernel.shutdown()
    reset()
    boot()

def reboot(event):
    """ reboot the bot, allowing statefull reboot (keeping connections alive). """
    if not botlib.space.cfg.reboot:
        event.reply("# reboot is not enabled.")
        return
    if not users.allowed(event.origin, "OPER"):
        event.reply("you are not allowed to give the reboot command. ")
        return
    event.announce("rebooting")
    real_reboot()

def reload(event):
    """ reload a plugin. """
    if not users.allowed(event.origin, "OPER"):
        event.reply("you are not allowed to give the reload command.")
        return
    if not event._parsed.rest:
        event.reply(",".join([x.split(".")[-1] for x in _kernel.modules()]))
        return
    for modname in _kernel.modules():
        if event._parsed.rest not in modname:
            continue
        event.reply(_kernel.reload(modname, True))

def restore(event):
    """ set deleted=False in selected records. """
    db = Db()
    nr = 0
    event.nodel = True
    for object in db.selected(event):
        object.deleted = False
        object.sync()
        nr += 1
    if not nr:
        event.reply("no results")
    event.ok(nr)

def rm(event):
    """ set deleted flag on objects. """
    db = Db()
    nr = 0
    for object in db.selected(event):
        object.deleted = True
        object.sync()
        nr += 1
    event.ok(nr)

def rss(event):
    """ add a rss url. """
    if not event._parsed.rest:
        event.reply("rss <item>")
        return
    o = Rss()
    o.rss = event._parsed.rest
    o.service = "rss"
    o.save()  
    event.ok(1)

def silent(event):
    """ put a bot into silent mode. """
    for bot in _fleet:
        if event.id() == bot.id():
            bot.cfg.silent = True
            bot.cfg.sync()
            event.reply("silent mode enabled.")

def shop(event):
    """ add a shopitem to the shopping list. """
    if not event._parsed.rest:
        event.reply("shop <item>")
        return
    o = Shop()
    o.shop = event._parsed.rest
    o.save()
    event.ok(1)

def show(event):
    import botlib.space
    if not event._parsed.rest:
        event.reply("choose one of %s" % ",".join(botlib.space.__all__))
        return
    try:
        item, value = event._parsed.rest.split(" ", 1)
    except:
        item = event._parsed.rest
        value = None
    if item == "bot":
        bot = _fleet.get_bot(event.id())
        event.reply(bot)
        return
    if item == "fleet":
        for bot in _fleet:
            event.reply(bot.id())
        return
    obj = getattr(botlib.space, item, None)
    if value:
        val = getattr(obj, value, None)
        event.reply(val)
    else:
        event.reply(obj)

def save(event):
    """ make a kernel dump. """
    botlib.space.alias.sync()
    botlib.space.kernel.sync()
    botlib.space.seen.sync()
    event.reply("saved")

def start(event):
    """ start a plugin. """
    if not users.allowed(event.origin, "OPER"):
        event.reply("you are not allowed to give the start command. ")
        return
    modnames = _kernel.modules()
    if not event._parsed.rest:
        res = set([x.split(".")[-1] for x in modnames])
        event.reply(sorted(res))
        return
    modname = event._parsed.args[0]
    name = "botlib.%s" % modname
    if name not in modnames:
        event.reply("no %s module found." % name)
        return
    mod = _kernel.reload(name, force=True, event=event)
    event.ok(sname(mod).lower())

def stop(event):
    """ stop a plugin. """
    if not users.allowed(event.origin, "OPER"):
        event.reply("you are not allowed to give the stop command.")
        return
    if not event._parsed.rest:
        event.reply("stop what ?")
        return
    name = "botlib.%s" % event._parsed.args[0]
    try:
        mod = _kernel._table[name]
        if "stop" in dir(mod):
            mod.stop(event)
        if "exit" in dir(mod):
            mod.exit(event)
        if "shutdown" in dir(mod):
            mod.shutdown(event)
    except (KeyError, ImportError):
        event.reply("no %s module found." % name)
        return
    _kernel.kill(name.upper())
    event.reply("stopped %s" % name)

def synchronize(event):
    clients = runtime.get("RSS", [])
    for client in clients:
        c = compose(client)
        seen = c.synchronize()
        event.reply("%s urls updated" % len(seen.urls))

def test(event):
    """ echo origin. """
    from .utils import stripped
    event.reply("hello %s" % stripped(event.origin))

def timer(event):
    """ timer command to schedule a text to be printed on a given time. stopwatch to measure elapsed time. """
    if not event._parsed.rest:
        event.reply("timer <string with time>")
        return
    seconds = 0
    line = ""
    for word in event._parsed.args:
        if word.startswith("+"):
             try:
                 seconds = int(word[1:])
             except:
                 event.reply("%s is not an integer" % seconds)
                 return
        else:
            line += word + " "
    if seconds:
        target = time.time() + seconds
    else:
        try:
            target = get_day(event._parsed.rest)
        except ENODATE:
            try:
                target = to_day(day())
            except ENODATE:
                pass
        try:
            hour =  get_hour(event._parsed.rest)
            if hour:
                target += hour
        except ENODATE:
            pass
    if not target or time.time() > target:
        event.reply("already passed given time.")
        return
    e = Event(event)
    e.services = "clock"
    e._prefix = "timer"
    e.txt = event._parsed.rest
    e.time = target
    e.done = False
    e.save()
    timer = Timer(target - time.time(), e.direct, e.txt)
    _kernel.launch(timer.start)
    event.ok(time.ctime(target))
    
def today(event):
    """ show objects logged for today.  """
    db = Db()
    event._parsed.start = to_day(day())
    event._parsed.end = time.time()
    nr = 0
    for object in db.selected(event):
        nr += 1
        event.display(object, event._parsed.args, str(nr))
    if not nr:
        event.reply("no results")

def todo(event):
    """ log a todo item. """
    if not event._parsed.rest:
        event.reply("todo <item>")
        return
    o = Todo()
    o.todo = event._parsed.rest
    o.save()
    event.ok(1)

def tomorrow(event):
    """ show todo items for tomorrow. """
    if not event._parsed.rest:
        event.reply("tomorrow <item>")
        return
    o = Tomorrow()
    o.tomorrow = event.txt.replace("tomorrow", "").strip()
    o.save()
    event.ok(1)

def uptime(event):
    """ show uptime. """
    event.reply("uptime is %s" % elapsed(time.time() - botlib._starttime))

def version(event):
    """ show version. """
    from botlib import __version__, __txt__
    event.reply("BOTLIB #%s - %s" % (__version__, __txt__))

def watch(event):
    if not event._parsed.rest:
        event.reply("watch <item>")
        return
    o = Watch()
    o.watch = event._parsed.rest
    o.save()
    event.ok(1)
    
def week(event):
    """ show last week's logged objects. """
    db = Db()
    event._parsed.start = to_day(day()) - 7 * 24 * 60 * 60
    event._parsed.end = time.time()
    nr = 0
    for object in db.selected(event):
        nr += 1
        event.display(object, event._parsed.args, str(nr))
    if not nr:
        event.reply("no results")

def whoami(event):
    """ show origin. """
    event.reply(event.origin)

def yesterday(event):
    """ show objects added yesterday. """
    db = Db()
    event._parsed.start = to_day(day()) - 24 * 60 * 60
    event._parsed.end = to_day(day())
    nr = 0
    for object in db.selected(event):
        nr += 1
        event.display(object, event._parsed.args, str(nr))
    if not nr:
        event.reply("no results")
