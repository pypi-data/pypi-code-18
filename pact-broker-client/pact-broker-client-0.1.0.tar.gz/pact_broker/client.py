import requests
import json

from . import urls
from requests.auth import HTTPBasicAuth


class BrokerClient:

    def __init__(
        self,
        *,
        broker_url,
        pact_dir='.',
        user=None,
        password=None,
        authentication=False
    ):
        self.broker_url = broker_url.rstrip('/')
        self.username = user
        self.password = password
        self.pact_dir = pact_dir
        self.authentication = authentication
        self._auth = None

        if self.authentication:
            if not (self.username and self.password):
                raise ValueError(
                    'When authentication is True, username and password '
                    'must be provided.'
                )
            else:
                self._auth = HTTPBasicAuth(self.username, self.password)

    def pull_pact(
        self,
        *,
        provider,
        consumer,
        version='latest'
    ):
        request_url = urls.PULL_CONTRACT_URL.format(
            broker_url=self.broker_url,
            provider=provider,
            consumer=consumer,
            version=version
        )

        response = requests.get(
            request_url,
            auth=self._auth
        )
        response.raise_for_status()
        saved_pact_path = self._save_contract(
            contract=response.json(),
            consumer=consumer,
            provider=provider
        )

        return response, f'Pact saved to {saved_pact_path}'

    def push_pact(self, *, pact_file, provider, consumer, version):
        request_url = urls.PUSH_CONTRACT_URL.format(
            broker_url=self.broker_url,
            provider=provider,
            consumer=consumer,
            version=version
        )

        with open(pact_file) as data_file:
            contract = json.load(data_file)

        response = requests.put(
            request_url,
            auth=self._auth,
            json=contract
        )
        response.raise_for_status()
        return response, (
            f'Pact with version:{version}'
            f'between {consumer} and {provider} pushed.'
        )

    def _save_contract(self, *, contract, consumer, provider):
        consumer = consumer.replace(' ', '_')
        provider = provider.replace(' ', '_')
        file_path = f'{self.pact_dir}/{provider}_{consumer}.json'.lower()

        with open(file_path, 'w') as contract_file:
            json.dump(contract, contract_file)

        return file_path
