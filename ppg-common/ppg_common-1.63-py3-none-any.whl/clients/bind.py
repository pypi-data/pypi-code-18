from ppg_common.clients import (
    BubblesClient, ButtercupClient, BlossomClient, PandoraClient
)
from ppg_common.clients.copperfield import CopperfieldClient


class BubblesProvider(object):

    client = BubblesClient
    service = 'bubbles'

    def __init__(self, config):
        self.config = config.get('services')

    def __call__(self, *args, **kwargs):
        data = self.config.get(self.service)
        return self.client(**data)


class ButtercupProvider(object):

    client = ButtercupClient
    service = 'buttercup'

    def __init__(self, config):
        self.config = config.get('services')

    def __call__(self, *args, **kwargs):
        data = self.config.get(self.service)
        return self.client(**data)


class BlossomProvider(object):

    client = BlossomClient
    service = 'blossom'

    def __init__(self, config):
        self.config = config.get('services')

    def __call__(self, *args, **kwargs):
        data = self.config.get(self.service)
        return self.client(**data)


class PandoraProvider(object):

    client = PandoraClient
    service = 'pandora'

    def __init__(self, config):
        self.config = config.get('services')

    def __call__(self, *args, **kwargs):
        data = self.config.get(self.service)
        return self.client(**data)


class CopperfieldProvider(object):

    client = CopperfieldClient
    service = 'copperfield'

    def __init__(self, config):
        self.config = config.get('services')

    def __call__(self, *args, **kwargs):
        data = self.config.get(self.service)
        return self.client(**data)


def bind_clients(providers, config, binder):
    for provider in providers:
        provider_instance = provider(config)
        binder.bind_to_provider(provider.client, provider_instance)
