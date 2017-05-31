# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import setRoles
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import TEST_USER_ID
from plone.testing import z2

import collective.wfadaptations


class CollectiveWfadaptationsLayer(PloneWithPackageLayer):

    def setUpPloneSite(self, portal):
        super(CollectiveWfadaptationsLayer, self).setUpPloneSite(portal)
        setRoles(portal, TEST_USER_ID, ['Manager'])


COLLECTIVE_WFADAPTATIONS_FIXTURE = CollectiveWfadaptationsLayer(
    zcml_package=collective.wfadaptations,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.wfadaptations:default',
    )


COLLECTIVE_WFADAPTATIONS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_WFADAPTATIONS_FIXTURE,),
    name='CollectiveWfadaptationsLayer:IntegrationTesting'
)


COLLECTIVE_WFADAPTATIONS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_WFADAPTATIONS_FIXTURE,),
    name='CollectiveWfadaptationsLayer:FunctionalTesting'
)


COLLECTIVE_WFADAPTATIONS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_WFADAPTATIONS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveWfadaptationsLayer:AcceptanceTesting'
)
