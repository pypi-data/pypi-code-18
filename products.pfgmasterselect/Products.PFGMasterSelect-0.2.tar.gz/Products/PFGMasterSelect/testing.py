from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.testing import z2
from zope.configuration import xmlconfig


class PFGMasterSelectLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.PloneFormGen
        import Products.DataGridField
        import Products.MasterSelectWidget
        import Products.PFGMasterSelect
        xmlconfig.file('configure.zcml', Products.PloneFormGen, context=configurationContext)
        xmlconfig.file('configure.zcml', Products.DataGridField, context=configurationContext)
        xmlconfig.file('configure.zcml', Products.MasterSelectWidget, context=configurationContext)
        xmlconfig.file('configure.zcml', Products.PFGMasterSelect, context=configurationContext)

        # Install products that use an old-style initialize() function
        z2.installProduct(app, 'Products.PloneFormGen')
        z2.installProduct(app, 'Products.DataGridField')
        z2.installProduct(app, 'Products.MasterSelectWidget')
        z2.installProduct(app, 'Products.PFGMasterSelect')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.PFGMasterSelect')
        z2.uninstallProduct(app, 'Products.MasterSelectWidget')
        z2.uninstallProduct(app, 'Products.DataGridField')
        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.PloneFormGen:default')
        applyProfile(portal, 'Products.DataGridField:default')
        applyProfile(portal, 'Products.MasterSelectWidget:default')
        applyProfile(portal, 'Products.PFGMasterSelect:default')

MASTER_SELECT_FIXTURE = PFGMasterSelectLayer()
MASTER_SELECT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MASTER_SELECT_FIXTURE,),
    name="PFGMasterSelectLayer:Integration"
)
MASTER_SELECT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MASTER_SELECT_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PFGMasterSelectLayer:Functional"
)
