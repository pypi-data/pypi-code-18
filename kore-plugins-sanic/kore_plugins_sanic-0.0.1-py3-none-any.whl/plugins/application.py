import logging

from sanic import Sanic

from kore.components.plugins.base import BasePluginComponent

log = logging.getLogger(__name__)


class SanicApplicationPluginComponent(BasePluginComponent):

    def get_services(self):
        return (
            ('config', self.config),
            ('application', self.application),
        )

    def config(self, container):
        config = container('config')

        return config.get('sanic', {})

    def application(self, container):
        # Uncomment when from_mapping support added
        # config = container('kore.components.sanic.config')

        app = Sanic(__name__)
        # from_mapping support https://github.com/channelcat/sanic/pull/619
        # app.config.from_mapping(**config)
        return app
