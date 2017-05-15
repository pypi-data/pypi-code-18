# mad/irc.py
#
#

""" IRC bot class. """

from .bot import Bot
from .event import Event
from .error import EDISCONNECT
from .handler import Handler
from .object import Object
from .space import cfg, fleet, kernel, partyline, users

from botlib import __version__

import logging
import _thread
import random
import socket
import queue
import time
import ssl
import re
import os

def init(event):
    bot = IRC()
    bot.start()
    return bot

class IRC(Bot):

    cc = "!"
    default = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._buffer = []
        self._handlers.register("004", self.connected)
        self._handlers.register("005", self.h005)
        self._handlers.register("ERROR", self.errored)
        self._handlers.register("352", self.h352)
        self._handlers.register("353", self.h353)
        self._handlers.register("366", self.h366)
        self._handlers.register("433", self.h433)
        self._handlers.register("513", self.h513)
        self._handlers.register("PING", self.pinged)
        self._handlers.register("PONG", self.ponged)
        self._handlers.register("QUIT", self.quited)
        self._handlers.register("INVITE", self.invited)
        self._handlers.register("PRIVMSG", self.privmsged)
        self._handlers.register("NOTICE", self.noticed)
        self._handlers.register("JOIN", self.joined)
        self._last = time.time()
        self._lastline = ""
        self._lock = _thread.allocate_lock()
        self._outqueue = queue.Queue()
        self._sock = None
        self._state.status = "running"
        self._userhosts = Object()
        self.started = False
        self.launch(self.output)

    def _bind(self):
        server = self.cfg.server
        try:
            self._oldsock.bind((server, 0))
        except socket.error:
            if not server:
                try:
                    socket.inet_pton(socket.AF_INET6, self.cfg.server)
                except socket.error:
                    pass
                else:
                    server = self.cfg.server
            if not server:
                try:
                    socket.inet_pton(socket.AF_INET, self.cfg.server)
                except socket.error:
                    pass
                else:
                    server = self.cfg.server
            if not server:
                ips = []
                try:
                    for item in socket.getaddrinfo(self.cfg.server, None):
                        if item[0] in [socket.AF_INET, socket.AF_INET6] and item[1] == socket.SOCK_STREAM:
                            ip = item[4][0]
                            if ip not in ips:
                                ips.append(ip)
                except socket.error:
                    pass
                else: server = random.choice(ips)
        return server

    def _connect(self):
        self.stopped = False
        if self.cfg.ipv6:
            self._oldsock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self._oldsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = self._bind() 
        self._cfg()
        self._error.status = ""

    def _cfg(self):
        self.blocking = True
        self._oldsock.setblocking(self.blocking)
        self._oldsock.settimeout(60.0)
        if not cfg.resume:
            logging.info("! connect %s:%s" % (self.cfg.server, self.cfg.port or 6667))
            self._oldsock.connect((self.cfg.server, int(str(self.cfg.port or 6667))))
        self._oldsock.setblocking(self.blocking)
        self._oldsock.settimeout(700.0)
        self.fsock = self._oldsock.makefile("r")
        if self.cfg.ssl:
            self._sock = ssl.wrap_socket(self._oldsock)
        else:
            self._sock = self._oldsock
        self._sock.setblocking(self.blocking)
        self._resume.fd = self._sock.fileno()
        if cfg.resume:
            os.set_inheritable(self._resume.fd, os.O_RDWR)
            self.register_fd(self._resume.fd)
        else:
            self.register_fd(self._sock.fileno())

    def _some(self):
        if self.cfg.ssl:
            inbytes = self._sock.read()
        else:
            inbytes = self._sock.recv(512)
        txt = str(inbytes, self.cfg.encoding)
        if txt == "":
            raise EDISCONNECT()
        self._lastline += txt
        splitted = self._lastline.split("\r\n")
        for s in splitted[:-1]:
            self._buffer.append(s)
            if "PING" not in s or "PONG" not in s:
                logging.info("< %s" % s.strip())
        self._lastline = splitted[-1]

    def announce(self, txt):
        for channel in self.channels:
            self._outqueue.put_nowait((channel, txt))

    def close(self):
        if self.ssl:
            self.oldsock.shutdown(1)
            self.oldsock.close()
        else:
            self._sock.shutdown(1)
            self._sock.close()
        self.fsock.close()

    def connect(self):
        if cfg.resume:
            self.resume()
            return
        for i in range(0, 4):
             self._counter.connect += 1
             try:
                 self._connect()
                 self.logon()
                 break
             except BrokenPipeError as ex:
                 logging.error("connect error to %s: %s" % (self.cfg.server, str(ex)))
             time.sleep(10.0 + self._counter.connect * 5)
             continue

    def dispatch(self, event):
        event.parse()
        for handler in self._handlers.get(event.command, []):
            handler(event)
        
    def event(self):
        if not self._buffer:
            self._some()
        line = self._buffer.pop(0)
        e = self.parsing(line.rstrip())
        e.btype = self.type
        return e

    def join(self, channel, password=""):
        if password:
            self.raw('JOIN %s %s' % (channel, password))
        else:
            self.raw('JOIN %s' % channel)
        if channel not in self.channels:
            self.channels.append(channel)

    def joinall(self):
        if self.cfg.channel:
            self.join(self.cfg.channel)
        for channel in self.channels:
            self.join(channel)

    def logon(self, *args):
        self.raw("NICK %s" % self.cfg.nick or "mad")
        self.raw("USER %s localhost %s :%s" % (self.cfg.username,
                                               self.cfg.server,
                                               self.cfg.realname))

    def out(self, channel, line):
        for txt in split_txt(line, 450):
            self.privmsg(channel, str(txt))
            if time.time() - self._last < 3.5:
                time.sleep(3.0) 

    def output(self):
        self._connected.wait()
        while self._state.status:
            args = self._outqueue.get()
            if not args or not self._state.status:
                break
            try:
                self.out(*args)
            except (EDISCONNECT,
                    BrokenPipeError, 
                    ConnectionResetError) as ex:
                        logging.error("# disconnect #%s %s %s" % (self._counter.push, self.cfg.server, str(ex)))
                        self._error.status = str(ex)
                        self._counter.push += 1
                        time.sleep(10 + self._counter.push * 3.0) 

    def parsing(self, txt):
        rawstr = str(txt)
        object = Event()
        object.txt = ""
        object.server = self.cfg.server
        object.cc = self.cc
        object.id = self.id()
        object.arguments = []
        arguments = rawstr.split()
        object.origin = arguments[0]
        if object.origin.startswith(":"):
            object.origin = object.origin[1:]
            if len(arguments) > 1:
                object.command = arguments[1]
            if len(arguments) > 2:
                    txtlist = []
                    adding = False
                    for arg in arguments[2:]:
                        if arg.startswith(":"):
                            adding = True
                            txtlist.append(arg[1:])
                            continue
                        if adding:
                            txtlist.append(arg)
                        else:
                            object.arguments.append(arg)
                    object.txt = " ".join(txtlist)
        else:
            object.command = object.origin
            object.origin = self.cfg.server
        try:
            object.nick, object.userhost = object.origin.split("!")
        except:
            pass
        if object.arguments:
            object.target = object.arguments[-1]
        else:
            object.target = ""
        if object.target.startswith("#"):
            object.channel = object.target
        if not object.txt and len(arguments) == 1:
            object.txt = arguments[1]
        if not object.txt:
            object.txt = rawstr.split(":")[-1]
        object.id = self.id()
        return object

    def part(self, channel):
        self.raw('PART %s' % channel)
        if channel in self.channels:
            self.channels.remove(channel)
            self.save()

    def raw(self, txt):
        if self._error.status:
            return
        if self._status == "error":
            return
        if not txt.endswith("\r\n"):
            txt += "\r\n"
        txt = txt[:512]
        txt = bytes(txt, "utf-8")
        logging.info("> %s" % txt)
        self._last = time.time()
        try:
            self._sock.send(txt)
            return
        except (BrokenPipeError, ConnectionResetError):
            pass
        except AttributeError:
            try:
                self._sock.write(txt)
                return
            except (BrokenPipeError, ConnectionResetError):
                return
        self._connected.clear()
        self._connected.wait()
        self.launch(self.connect)

    def register_fd(self, f):
        try:
            fd = f.fileno()
        except:
            fd = f
        if not fd:
            return fd
        logging.warn("# engine on %s" % str(fd))
        self._poll.register(fd)
        self._resume.fd = fd
        return fd

    def resume(self):
        fd = None
        for bot in fleet:
            if "type" in bot and bot["type"].lower() != self.id():
                continue
            try:
                fd = bot["_resume"]["fd"]
            except:
                continue
            self.channels = bot["channels"]
        if not fd:
            self.announce("resume failed")
            return
        logging.warn("# resume %s %s" % (fd, ",".join([str(x) for x in self.channels])))
        if self.cfg.ipv6:
            self._oldsock = socket.fromfd(fd, socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self._oldsock = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
        self._cfg()
        self.start()
        self.announce("done")

    def say(self, channel, txt):
        self._outqueue.put_nowait((channel, txt))

    def start(self, *args, **kwargs):
        self.connect()
        super().start(*args, **kwargs)

    def stop(self, close=True):
        super().stop()
        self._state.status = ""
        self._outqueue.put(None)
  
    def noticed(self, event):
        pass

    def connected(self, event):
        if "servermodes" in self.cfg:
            self.raw("MODE %s %s" % (self.cfg.nick, self.cfg.servermodes))
        logging.warn("# connected %s:%s" % (self.cfg.server, self.cfg.port))
        self.joinall()
        self._error.status = ""
        self._connected.ready()

    def invited(self, event):
        self.join(event.channel)

    def joined(self, event):
        self.who(event.channel)
        if event.channel not in self.channels:
            self.channels.append(event.channel)

    def errored(self, event):
        self._error.status = event.txt
        logging.warn("# error %s" % event.txt)

    def pinged(self, event):
        self.pongcheck = True
        self.pong(event.txt)
        self.ready()

    def ponged(self, event):
        self.pongcheck = False

    def quited(self, event):
        if "Ping timeout" in event.txt and event.nick == self.cfg.nick:
            self.connect()

    def privmsged(self, event):
        if event.txt.startswith("\001DCC"):
            self.dccconnect(event)
            return
        elif event.txt.startswith("\001VERSION"):
            self.ctcpreply(event.nick, "VERSION BOTLIB #%s - http://pypi.python.org/pypi/botlib" % __version__)
            return
        kernel.put(event)
        
    def ctcped(self, event): pass

    def h001(self, event):
        pass

    def h002(self, event):
        pass

    def h003(self, event):
        pass

    def h004(self, event):
        pass

    def h005(self, event):
        pass

    def h352(self, event):
        args = event.arguments
        self._userhosts[args[5]] = args[2] + "@" + args[3]

    def h353(self, event):
        pass

    def h366(self, event):
        pass 

    def h433(self, event):
        self.donick(event.target + "_")
      
    def h513(self, event):
        self.raw("PONG %s" % event.txt.split()[-1])

    def donick(self, name):
        self.raw('NICK %s\n' % name[:16])
        self.cfg.nick = name
        self.sync()

    def who(self, channel):
        self.raw('WHO %s' % channel)

    def names(self, channel):
        self.raw('NAMES %s' % channel)

    def whois(self, nick):
        self.raw('WHOIS %s' % nick)

    def privmsg(self, channel, txt):
        self.raw('PRIVMSG %s :%s' % (channel, txt))

    def voice(self, channel, nick):
        self.raw('MODE %s +v %s' % (channel, nick))

    def doop(self, channel, nick):
        self.raw('MODE %s +o %s' % (channel, nick))

    def delop(self, channel, nick):
        self.raw('MODE %s -o %s' % (channel, nick))

    def quit(self, reason='https://pikacode.com/bart/mad'):
        self.raw('QUIT :%s' % reason)

    def notice(self, channel, txt):
        self.raw('NOTICE %s :%s' % (channel, txt))

    def ctcp(self, nick, txt):
        self.raw("PRIVMSG %s :\001%s\001" % (nick, txt))

    def ctcpreply(self, channel, txt):
        self.raw("NOTICE %s :\001%s\001" % (channel, txt))

    def action(self, channel, txt):
        self.raw("PRIVMSG %s :\001ACTION %s\001" % (channel, txt))

    def getchannelmode(self, channel):
        self.raw('MODE %s' % channel)

    def settopic(self, channel, txt):
        self.raw('TOPIC %s :%s' % (channel, txt))

    def ping(self, txt):
        self.raw('PING :%s' % txt)

    def pong(self, txt):
        self.raw('PONG :%s' % txt)

    def dcced(self, event, s):
        s.send(bytes('Welcome to BOTLIB ' + event.nick + " !!\n", self.cfg.encoding))
        self.launch(self.dccloop, event, s)

    def dccloop(self, event, s):
        sockfile = s.makefile('rw')
        s.setblocking(True)
        self.register_fd(s.fileno())
        partyline.register(event.origin, sockfile)
        while 1:
            try:
                res = sockfile.readline()
                if not res:
                    break
                res = res.rstrip()
                logging.info("< DCC %s %s" % (event.origin, res))
                e = Event()
                e._socket = sockfile
                e.cc = ""
                e.btype = "irc"
                e.server = event.server
                e.txt = res
                e.origin = event.origin
                e.parse()
                kernel.put(e)
            except socket.timeout:
                time.sleep(0.01)
            except socket.error as ex:
                if ex.errno in [socket.EAGAIN, ]:
                    continue
                else:
                    raise
        sockfile.close()
        del partyline[event.origin]

    def dccconnect(self, event):
        event.parse()
        addr = event._parsed.args[2] 
        port = event._parsed.args[3][:-1]
        port = int(port)
        if re.search(':', addr):
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
        self.dcced(event, s)

def split_txt(what, l=450):
    z = ""
    what = str(what)
    for txt in what.split("\n"):
        if len(txt) < l:
            yield txt
        else:
            for y in txt.split():
                if len(y) + len(z) < l:
                    z += " " + y
                    continue
                yield z.strip()
                z = ""
    if z:
        yield z.strip()

