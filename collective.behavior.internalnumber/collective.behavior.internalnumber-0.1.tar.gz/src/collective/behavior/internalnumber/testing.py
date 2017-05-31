# -*- coding: utf-8 -*-
from plone import api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2

import collective.behavior.internalnumber


class CollectiveBehaviorInternalnumberLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.behavior.internalnumber, name='testing.zcml')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.behavior.internalnumber:testing')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        content = api.content.create(container=portal, id='tt1', type='testtype', title='My content',
                                     internal_number='AA123')
        content.reindexObject()


COLLECTIVE_BEHAVIOR_INTERNALNUMBER_FIXTURE = CollectiveBehaviorInternalnumberLayer()


COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_BEHAVIOR_INTERNALNUMBER_FIXTURE,),
    name='CollectiveBehaviorInternalnumberLayer:IntegrationTesting'
)


COLLECTIVE_BEHAVIOR_INTERNALNUMBER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_BEHAVIOR_INTERNALNUMBER_FIXTURE,),
    name='CollectiveBehaviorInternalnumberLayer:FunctionalTesting'
)


COLLECTIVE_BEHAVIOR_INTERNALNUMBER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_BEHAVIOR_INTERNALNUMBER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveBehaviorInternalnumberLayer:AcceptanceTesting'
)
