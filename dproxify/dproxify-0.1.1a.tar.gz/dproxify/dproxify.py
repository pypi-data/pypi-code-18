# dproxify: an object daemon proxifier module
# Written by Francesco Palumbo aka phranz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.




import os
import sys
import types
import pickle
import traceback

from . import utils
from . import tcputils


class DaemonNotRunningOnSocketPathException(Exception):
    pass


class DaemonCreationException(Exception):
    pass


class ProxyCreationException(Exception):
    pass


class DaemonCannotPassUnpickleableObjectException(Exception):
    def __init__(self, exc):
        self.exc = exc


class DaemonIsAlredyRunningException(Exception):
    '''
    Exception raised in the case daemon
    is alredy running. Instances have
    "self.pid" (which is the PID of the daemon),
    and "self.msg" (which is a message) as attributes.
    '''

    def __init__(self, pid, msg):
        self.pid = pid
        self.msg = msg


_DAEMON_STOP_TOKEN = '__DAEMON_STOP'


_excluded_special_methods = [
    '__init__', '__new__',
    '__class__', '__hash__',
    '__getattr', '__getattribute__',
]



_special_daemon_methods = {
    '_get_obj_infos': lambda obj, *args, **kargs: \
                          (obj.__class__.__name__,
                           ['__getattr__'] + [m for m in dir(obj)
                            if (m not in _excluded_special_methods)
                            and callable(getattr(obj, m))]),

    '_stop_daemon'  : lambda obj, *args, **kargs: \
                          _DAEMON_STOP_TOKEN,
}


def get_proxy_object(sockpath, raise_exceptions=False):
    '''
    Returns a fake/proxy of the original object (and communicating
    with the daemon by using AFUnix sockets) given "sockpath".
    If "raise_exceptions" is True, the proxy will raise original
    exception, else it will simply return the exception object.
    '''

    sockpath = os.path.abspath(sockpath)

    sock = None

    try:
        sock = tcputils.make_UDS_socket_client(sockpath)

    except FileNotFoundError as e:
        raise DaemonNotRunningOnSocketPathException('Daemon socket %s does not exist!' %sockpath) from e

    except OSError as e:
        raise ProxyCreationException('Cannot create the proxy.') from e

    tcputils.msgwrite(sock, pickle.dumps(('_get_obj_infos', (), {})))
    class_name, method_names = pickle.loads(tcputils.msgread(sock))

    proxycls = type('DaemonProxified' + class_name, (), {})

    def sockify_procedure_by_name(method_name):
        def sockified_procedure(inst, *args, **kargs):
            tcputils.msgwrite(sock, pickle.dumps((method_name, args, kargs)))
            output = pickle.loads(tcputils.msgread(sock))

            if raise_exceptions and isinstance(output, Exception):
                raise output

            return output

        sockified_procedure.__name__ = method_name
        return sockified_procedure

    method_names += list(_special_daemon_methods.keys())

    for m in method_names:
        setattr(proxycls, m, sockify_procedure_by_name(m))


    return proxycls()


def _serve(serv_sock, obj):
    '''
    Procedure to daemonize.
    "obj" is the object to daemonize.
    '''

    running = True

    while running:
        csock, caddr = serv_sock.accept()

        while running:
            output = None
            action = None
            raw    = None

            try:
                raw = tcputils.msgread(csock)

            except tcputils.SocketMessageReadException:
                break

            data  = pickle.loads(raw)
            meth  = data[0]
            args  = data[1]
            kargs = data[2]


            if meth in _special_daemon_methods:
                output  = _special_daemon_methods[meth](obj, *args, **kargs)
                running = output != _DAEMON_STOP_TOKEN

            else:
                try:
                    attr = None

                    if meth == '__getattr__':
                        attr = getattr(obj, *args, **kargs)
                    else:
                        attr = getattr(obj, meth)

                    output = attr(*args, **kargs) if callable(attr) else attr

                except:
                    t, v, tb = sys.exc_info()

                    call_info = '\n' + ''.join(traceback.format_tb(tb)).rstrip()

                    v.args = (v.args[0] + call_info,)
                    output = v

            try:
                output = pickle.dumps(output)

            except:
                t, v, tb = sys.exc_info()
                output = pickle.dumps(DaemonCannotPassUnpickleableObjectException(v))

            tcputils.msgwrite(csock, output)

        csock.close()


def daemonize_object(obj, sockpath, pidfile, fds=(None, None, None), shut_proc=lambda: 0, shut_proc_args=()):
    '''
    Creates a daemon and "loads" the object "obj" into it.

    Arguments:

    obj -- the object to daemonize.

    sockpath -- the choosen socket path (AFUnix).

    pidfile -- the choosen path for storing the PID of the daemon.


    Keyword arguments:

    fds -- A tuple of three file descriptors which represent
           the new stdin, stdout and stderr (in order) of the daemon.
           All three defaults to 'None', meaning stdin, stdout
           and stderr all points to /dev/null

    shut_proc -- The procedure to execute at shutdown.

    shut_proc_args -- Arguments of the shutdown procedure.



    Additional infos:

    Note that at shutdown, the daemon takes care of removing the pidfile
    and the socket file, so it is not necessary to manually remove those.
    It tries to also handle SIGINT and SITERM automatically for the purpose
    of exit gracefully.

    '''

    sockpath = os.path.abspath(sockpath)
    pidfile  = os.path.abspath(pidfile)

    if os.path.exists(pidfile):
        pid = utils.cat(pidfile)

        if utils.isrunning(pid):
            raise DaemonIsAlredyRunningException(int(pid), 'Daemon is running with a PID of %s' % pid)


    server_sock = None

    try:
        server_sock = tcputils.make_UDS_socket_server(sockpath)

    except OSError as e:
        if e.errno == 98:
            try:
                raise tcputils.SocketFileAlredyInUseException('%s is alredy in use or is not a socket!' % sockpath) \
                      from e

            except tcputils.SocketFileAlredyInUseException as s:
                raise DaemonCreationException('Cannot create the daemon') \
                      from s

        raise DaemonCreationException('Cannot create the daemon') \
              from e


    def shutdown_proc():
        server_sock.close()
        os.remove(sockpath)
        shut_proc(*shut_proc_args)


    utils.daemonize(pidfile, newfds=fds,
                    procedure=_serve, args=(server_sock, obj),
                    shutdown=shutdown_proc)
