#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.session.telnet_session import TelnetSession


class ASATelnetSession(TelnetSession):
    def __init__(self, host, username, password, port=None, on_session_start=None, *args, **kwargs):
        super(ASATelnetSession, self).__init__(host, username, password, port, on_session_start, *args, **kwargs)

    def get_local_address(self):
        """ Determine local device (device that initiate connection) IP address """

        return self._handler.sock.getsockname()[0]
