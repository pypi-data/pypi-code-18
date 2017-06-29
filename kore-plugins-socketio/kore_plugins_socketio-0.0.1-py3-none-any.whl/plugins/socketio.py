import logging

from socketio import AsyncServer

from kore.components.plugins.base import BasePluginComponent

log = logging.getLogger(__name__)


class SocketIOPluginComponent(BasePluginComponent):

    def get_services(self):
        return (
            ('config', self.config),
            ('async_server', self.async_server),
        )

    def config(self, container):
        config = container('config')

        return config.get('socketio', {})

    def async_server(self, container):
        engineio_options = container('kore.components.socketio.config')

        srv = AsyncServer(**engineio_options)
        return srv
