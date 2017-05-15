# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base.domain import Domain
from twilio.rest.preview.marketplace import Marketplace
from twilio.rest.preview.sync import Sync
from twilio.rest.preview.wireless import Wireless


class Preview(Domain):

    def __init__(self, twilio):
        """
        Initialize the Preview Domain

        :returns: Domain for Preview
        :rtype: twilio.rest.preview.Preview
        """
        super(Preview, self).__init__(twilio)

        self.base_url = 'https://preview.twilio.com'

        # Versions
        self._sync = None
        self._wireless = None
        self._marketplace = None

    @property
    def sync(self):
        """
        :returns: Version sync of preview
        :rtype: twilio.rest.preview.sync.Sync
        """
        if self._sync is None:
            self._sync = Sync(self)
        return self._sync

    @property
    def wireless(self):
        """
        :returns: Version wireless of preview
        :rtype: twilio.rest.preview.wireless.Wireless
        """
        if self._wireless is None:
            self._wireless = Wireless(self)
        return self._wireless

    @property
    def marketplace(self):
        """
        :returns: Version marketplace of preview
        :rtype: twilio.rest.preview.marketplace.Marketplace
        """
        if self._marketplace is None:
            self._marketplace = Marketplace(self)
        return self._marketplace

    @property
    def services(self):
        """
        :rtype: twilio.rest.preview.sync.service.ServiceList
        """
        return self.sync.services

    @property
    def commands(self):
        """
        :rtype: twilio.rest.preview.wireless.command.CommandList
        """
        return self.wireless.commands

    @property
    def rate_plans(self):
        """
        :rtype: twilio.rest.preview.wireless.rate_plan.RatePlanList
        """
        return self.wireless.rate_plans

    @property
    def sims(self):
        """
        :rtype: twilio.rest.preview.wireless.sim.SimList
        """
        return self.wireless.sims

    @property
    def available_add_ons(self):
        """
        :rtype: twilio.rest.preview.marketplace.available_add_on.AvailableAddOnList
        """
        return self.marketplace.available_add_ons

    @property
    def installed_add_ons(self):
        """
        :rtype: twilio.rest.preview.marketplace.installed_add_on.InstalledAddOnList
        """
        return self.marketplace.installed_add_ons

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview>'
