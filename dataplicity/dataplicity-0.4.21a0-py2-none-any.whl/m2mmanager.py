"""Manages M2M connections."""

from __future__ import print_function
from __future__ import unicode_literals

import logging
import subprocess
import threading

from . import constants
from .m2m import WSClient, EchoService
from .m2m.remoteprocess import RemoteProcess


log = logging.getLogger('m2m')


class Terminal(object):
    """Configured terminal information."""

    def __init__(self, name, command, user=None, group=None):
        self.name = name
        self.command = command
        self.user = user
        self.group = group
        self.processes = []

    def __repr__(self):
        return "<terminal '{}' command='{}'>".format(self.name, self.command)

    def _prune_closed(self):
        """Remove closed processes."""
        self.processes[:] = [process for process in self.processes if not process.is_closed]

    def launch(self, channel, size=None):
        """Launch a terminal instance."""
        if size is None:
            size = [80, 24]
        self._prune_closed()
        log.debug('opening terminal %s', self.name)
        remote_process = None
        try:
            remote_process = RemoteProcess(self.command,
                                           channel,
                                           user=self.user,
                                           group=self.group,
                                           size=size)
        except:
            log.exception("error launching terminal process '%s'", self.command)
            if remote_process is not None:
                try:
                    remote_process.close()
                except:
                    pass
        else:
            self.processes.append(remote_process)
            process_thread = threading.Thread(target=remote_process.run)
            process_thread.start()
            log.info("launched remote process %r over %r", self, channel)

    def close(self):
        self._prune_closed()
        for process in self.processes:
            log.debug('closing %r', self)
            try:
                if not process.is_closed:
                    log.debug('closing %r', self)
                    process.close()
            except:
                log.exception('error closing %s', process)
        del self.processes[:]


class M2MManager(object):
    """Manages M2M Services."""

    def __init__(self, client, url, identity=None):
        self.client = client
        self.url = url
        self.identity = identity
        self.terminals = {}
        self.notified_identity = None
        self.m2m_client = WSClient(self, url)

    @classmethod
    def init(cls, client, m2m_url=None):
        """Set up the m2m manager for Dataplicity."""
        url = m2m_url or constants.M2M_URL
        manager = cls(client, url)
        manager.m2m_client.start()
        manager.add_terminal('shell', 'bash -i')
        return manager

    def restart_agent(self):
        """Restart the agent."""
        self.client.exit()

    def on_client_close(self):
        """Client is closing, shutdown all terminals."""
        for terminal in self.terminals.values():
            terminal.close()

    def set_identity(self, identity):
        """Set the m2m identity, and also notifies the dataplicity server if required."""
        self.identity = identity
        if identity and identity != self.notified_identity:
            log.info('m2m identity changed (%r)', identity)
            self.notified_identity = self.client.set_m2m_identity(identity)

    def on_sync(self, batch):
        """Called by sync, so it can inject commands in to the batch request."""
        # Send the m2m identity on every sync
        # This shouldn't be necessary, but could mitigate any screw ups server side
        # NOTE: not currently called in agent
        if self.identity:
            log.debug('syncing m2m identity (%s)', self.identity)
            batch.notify('m2m.associate', identity=self.identity)

    def close(self):
        log.debug('m2m manager close')
        if self.m2m_client is not None:
            self.m2m_client.close()

    def add_terminal(self, name, remote_process, user=None, group=None):
        """Add a terminal for a remote process."""
        log.debug("adding terminal '%s' %s", name, remote_process)
        self.terminals[name] = Terminal(name, remote_process, user=user, group=group)

    def get_terminal(self, name):
        """Get a named terminal."""
        return self.terminals.get(name, None)

    def on_instruction(self, sender, data):
        """Instructions sent by privileged client."""
        log.debug("instruction %r from %s", data, sender)
        action = data['action']
        if action == 'sync':
            self.client.sync()
        elif action == 'open-terminal':
            port = data['port']
            terminal_name = data['name']
            size = data.get('size', None)
            self.open_terminal(terminal_name, port, size=size)
        elif action == "open-echo":
            port = data['port']
            self.open_echo_service(port)
        elif action == 'open-portforward':
            service = data['service']
            route = data['route']
            self.open_portforward(service, route)
        elif action == 'open-portredirect':
            device_port = data['device_port']
            m2m_port = data['m2m_port']
            self.client.port_forward.redirect_port(device_port, m2m_port)
        elif action == 'reboot-device':
            log.debug('reboot requested')
            self.reboot()
        # Unrecognized instructions are ignored

    def open_terminal(self, name, port, size=None):
        """Open a new terminal."""
        terminal = self.get_terminal(name)
        if terminal is None:
            log.warning("no terminal called '%s'", name)
            return
        terminal.launch(self.m2m_client.get_channel(port), size=size)

    def open_echo_service(self, port):
        """Open an echo service (ping)."""
        log.debug('opening echo service on m2m port %s', port)
        EchoService(self.m2m_client.get_channel(port))

    def open_portforward(self, service, route):
        """Open a port forward service."""
        self.client.port_forward.open_service(service, route)

    def reboot(self):
        """Initiate a reboot."""
        # TODO: consider initiating a graceful shutdown of dpcore that ends in a rebooot
        command = '/usr/bin/sudo /sbin/reboot'
        log.debug('rebooting!')
        # Why not subprocess.call? Because it will block this process and prevent graceful exit!
        pid = subprocess.Popen(command.split()).pid
        log.debug('opened reboot process %s', pid)
