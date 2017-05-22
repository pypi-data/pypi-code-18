import sparc.testing
from zope import component
from zope.component.testlayer import ZCMLFileLayer
from zope import interface
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyRegistry
from zope.schema.vocabulary import setVocabularyRegistry


#Copied from Zope2.App.schema
@interface.implementer(IVocabularyRegistry)
class Zope2VocabularyRegistry(object):
    """IVocabularyRegistry that supports global and local utilities.
    """

    __slots__ = ()

    def get(self, context, name):
        """See zope.schema.interfaces.IVocabularyRegistry.
        """
        factory = component.getUtility(IVocabularyFactory, name)
        return factory(context)

#Copied from Zope2.App.schema
def configure_vocabulary_registry():
    setVocabularyRegistry(Zope2VocabularyRegistry())

class SparcZCMLFileLayer(ZCMLFileLayer):
    def setUp(self):
        super(SparcZCMLFileLayer, self).setUp()
        configure_vocabulary_registry()
    def tearDown(self):
        super(SparcZCMLFileLayer, self).tearDown()
        

SPARC_INTEGRATION_LAYER = SparcZCMLFileLayer(sparc.testing)