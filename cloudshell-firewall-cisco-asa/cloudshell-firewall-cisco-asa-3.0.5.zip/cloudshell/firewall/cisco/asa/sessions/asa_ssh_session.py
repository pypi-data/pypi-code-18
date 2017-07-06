#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.session.ssh_session import SSHSession


class ASASSHSession(SSHSession):
    def __init__(self, host, username, password, port=None, on_session_start=None, *args, **kwargs):
        super(ASASSHSession, self).__init__(host, username, password, port, on_session_start, *args, **kwargs)

    def connect(self, prompt, logger):
        """Connect to device through ssh
        :param prompt: expected string in output
        :param logger: logger
        """
        try:
            super(ASASSHSession, self).connect(prompt, logger)
        except Exception:
            self.disconnect()
            raise

    def get_local_address(self):
        """ Determine local device (device that initiate connection) IP address """

        return self._handler._transport.sock.getsockname()[0]
