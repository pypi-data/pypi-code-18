import errno
import os
import pty
import signal
import tty
import array
import fcntl
import termios
import select
import io
import shlex
import sys
import struct
import re
import requests
import json

from asciinema.term import raw
from codelynx.api import Api


class PtyRecorder:

    def record_command(self, command, output, env=os.environ):

        master_fd = None
        # Read buffer, max = 1024
        rbuf = 1024
        get_ecode = False
        cmdlast = ''
        ecode = ''

        def _set_pty_size():
            '''
            Sets the window size of the child pty based on the window size
            of our own controlling terminal.
            '''

            # Get the terminal size of the real terminal, set it on the
            # pseudoterminal.
            if os.isatty(pty.STDOUT_FILENO):
                buf = array.array('h', [0, 0, 0, 0])
                fcntl.ioctl(pty.STDOUT_FILENO, termios.TIOCGWINSZ, buf, True)
                fcntl.ioctl(master_fd, termios.TIOCSWINSZ, buf)
            else:
                buf = array.array('h', [24, 80, 0, 0])
                fcntl.ioctl(master_fd, termios.TIOCSWINSZ, buf)

        def _write_stdout(data):
            '''
            Writes to stdout as if the child process had written the data.
            '''

            # collect environment info
            session_id = os.environ._data[b'TERM_SESSION_ID'].decode()
            # google_api_key = os.environ._data[b'GOOGLE_API_KEY'].decode()
            terminal_user = os.environ._data[b'USER'].decode()
            shell = os.environ._data[b'SHELL'].decode()
            term_program = os.environ._data[b'TERM_PROGRAM'].decode()

            # post data to server
            codelynx_api.handle_data('data', quiet=True, rec=data.decode(),
                                     session_id=session_id, shell=shell,
                                     terminal_user=terminal_user,
                                     term_program=term_program)
            # print data on terminal
            os.write(pty.STDOUT_FILENO, data)

        def _handle_master_read(data):
            '''Handles new data on child process stdout.'''

            # Add time, decoder to data
            _write_stdout(data)

        def _write_master(data):
            '''Writes to the child process from its controlling terminal.'''

            # Record input char
            # codelynx_api.handle_data(str(data, 'utf-8'), '')

            while data:
                n = os.write(master_fd, data)
                data = data[n:]

        def _handle_stdin_read(data):
            '''Handles new data on child process stdin.'''
            _write_master(data)

        def _signals(signal_list):
            old_handlers = []
            for sig, handler in signal_list:
                old_handlers.append((sig, signal.signal(sig, handler)))
            return old_handlers

        def _copy(signal_fd):
            '''Main select loop.

            Passes control to _master_read() or _stdin_read()
            when new data arrives.
            '''

            fds = [master_fd, pty.STDIN_FILENO, signal_fd]
            cmdin = ''
            cmdout = ''
            cmdcode = ''
            nonlocal cmdlast

            while True:
                try:
                    rfds, wfds, xfds = select.select(fds, [], [])

                except OSError as e:  # Python >= 3.3
                    if e.errno == errno.EINTR:
                        continue
                except select.error as e:  # Python < 3.3
                    if e.args[0] == 4:
                        continue

                # Output
                if master_fd in rfds:
                    if cmdlast == b'\r':
                        data = os.read(master_fd, rbuf)
                        cmdin = ''
                        cmdout = str(data, 'utf-8')

                    else:
                        data = os.read(master_fd, rbuf)

                    if not data:  # Reached EOF.
                        fds.remove(master_fd)
                    else:
                        _handle_master_read(data)

                # Input
                if pty.STDIN_FILENO in rfds:
                    data = os.read(pty.STDIN_FILENO, rbuf)
                    cmdlast = data
                    cmdin += str(data, 'utf-8')
                    if not data:
                        fds.remove(pty.STDIN_FILENO)
                    else:
                        _handle_stdin_read(data)

                if signal_fd in rfds:
                    data = os.read(signal_fd, rbuf)
                    if data:
                        signals = struct.unpack('%uB' % len(data), data)
                        for sig in signals:
                            if sig in [signal.SIGCHLD,
                                       signal.SIGHUP,
                                       signal.SIGTERM,
                                       signal.SIGQUIT]:
                                os.close(master_fd)
                                return
                            elif sig == signal.SIGWINCH:
                                _set_pty_size()

        pid, master_fd = pty.fork()

        if pid == pty.CHILD:
            os.execvpe(command[0], command, env)

        pipe_r, pipe_w = os.pipe()
        flags = fcntl.fcntl(pipe_w, fcntl.F_GETFL, 0)
        flags = flags | os.O_NONBLOCK
        flags = fcntl.fcntl(pipe_w, fcntl.F_SETFL, flags)

        signal.set_wakeup_fd(pipe_w)

        old_handlers = _signals(map(lambda s: (s, lambda signal, frame: None),
                                    [signal.SIGWINCH,
                                     signal.SIGCHLD,
                                     signal.SIGHUP,
                                     signal.SIGTERM,
                                     signal.SIGQUIT]))

        _set_pty_size()

        with raw(pty.STDIN_FILENO):
            try:
                codelynx_api = Api()
                _copy(pipe_r)
            except (IOError, OSError):
                pass

        _signals(old_handlers)

        os.waitpid(pid, 0)
        output.close()
