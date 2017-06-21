# -*- coding: utf-8 -*-
from gapi.facade.calls import FacadeCalls
from gapi.facade.result_fields import AdwInteger, AdwUnicode, AdwBoolean, AdwANSI


class GetTrafficEstimator(FacadeCalls):
    # TODO experimental
    params = dict(selector=None)
    returns = (
        AdwInteger('CustomerId'),
        AdwUnicode('Name'),
        # AdwUnicode('CompanyName'),
        #       The companyName field has been removed. This field only contained outdated data and was read-only.
        #       For a descriptive identifier of an account, you can use Customer.descriptiveName.
        #       https://developers.google.com/adwords/api/docs/guides/migration/v201609?hl=ru
        AdwBoolean('CanManageClients'),
        AdwANSI('CurrencyCode'),
        AdwANSI('DateTimeZone'),
    )

    def handle(self):
        selector = self._get_param('selector')
        return self.service('get_traffic_estimator', params=dict(selector=selector), )
