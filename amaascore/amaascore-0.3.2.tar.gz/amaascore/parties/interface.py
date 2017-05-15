from __future__ import absolute_import, division, print_function, unicode_literals

import json
import logging

from amaascore.config import ENVIRONMENT
from amaascore.core.amaas_model import json_handler
from amaascore.core.interface import Interface
from amaascore.parties.utils import json_to_party


class PartiesInterface(Interface):

    def __init__(self, environment=ENVIRONMENT, logger=None, endpoint=None):
        self.logger = logger or logging.getLogger(__name__)
        super(PartiesInterface, self).__init__(endpoint=endpoint, endpoint_type='parties', environment=environment)

    def new(self, party):
        self.logger.info('New Party - Asset Manager: %s - Party ID: %s', party.asset_manager_id, party.party_id)
        url = '%s/parties/%s' % (self.endpoint, party.asset_manager_id)
        response = self.session.post(url, json=party.to_interface())
        if response.ok:
            party = json_to_party(response.json())
            return party
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def amend(self, party):
        self.logger.info('Amend Party - Asset Manager: %s - Party ID: %s', party.asset_manager_id, party.party_id)
        url = '%s/parties/%s/%s' % (self.endpoint, party.asset_manager_id, party.party_id)
        response = self.session.put(url, json=party.to_interface())
        if response.ok:
            party = json_to_party(response.json())
            return party
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def partial(self, asset_manager_id, party_id, updates):
        self.logger.info('Partial Amend Asset - Asset Manager: %s - Party ID: %s', asset_manager_id,
                         party_id)
        url = '%s/parties/%s/%s' % (self.endpoint, asset_manager_id, party_id)
        # Setting handler ourselves so we can be sure Decimals work
        response = self.session.patch(url, data=json.dumps(updates, default=json_handler), headers=self.json_header)
        if response.ok:
            party = json_to_party(response.json())
            return party
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def retrieve(self, asset_manager_id, party_id):
        self.logger.info('Retrieve Party - Asset Manager: %s - Party ID: %s', asset_manager_id, party_id)
        url = '%s/parties/%s/%s' % (self.endpoint, asset_manager_id, party_id)
        response = self.session.get(url)
        if response.ok:
            return json_to_party(response.json())
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def deactivate(self, asset_manager_id, party_id):
        self.logger.info('Deactivate Party - Asset Manager: %s - Party ID: %s', asset_manager_id, party_id)
        url = '%s/parties/%s/%s' % (self.endpoint, asset_manager_id, party_id)
        json = {'party_status': 'Inactive'}
        response = self.session.patch(url, json=json)
        if response.ok:
            self.logger.info(response.text)
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def search(self, asset_manager_ids=None, party_ids=None):
        self.logger.info('Search Parties - Asset Manager(s): %s', asset_manager_ids)
        search_params = {}
        # Potentially roll this into a loop through args rather than explicitly named - depends on additional validation
        if asset_manager_ids:
            search_params['asset_manager_ids'] = asset_manager_ids
        if party_ids:
            search_params['party_ids'] = party_ids
        url = self.endpoint + '/parties'
        response = self.session.get(url, params=search_params)
        if response.ok:
            parties = [json_to_party(json_party) for json_party in response.json()]
            self.logger.info('Returned %s Parties.', len(parties))
            return parties
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def parties_by_asset_manager(self, asset_manager_id):
        self.logger.info('Retrieve Parties by Asset Manager: %s', asset_manager_id)
        url = '%s/parties/%s' % (self.endpoint, asset_manager_id)
        response = self.session.get(url)
        if response.ok:
            parties = [json_to_party(json_party) for json_party in response.json()]
            self.logger.info('Returned %s Parties.', len(parties))
            return parties
        else:
            self.logger.error(response.text)
            response.raise_for_status()
