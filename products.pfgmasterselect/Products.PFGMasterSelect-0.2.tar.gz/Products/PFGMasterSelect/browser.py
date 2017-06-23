import json

import logging

import Products
from App.Common import aq_base
from Products.Archetypes import DisplayList
from Products.CMFCore import Expression
from Products.CMFCore.Expression import getExprContext
from Products.Five import BrowserView
from Products.MasterSelectWidget.browser import JSONValuesForAction, SetupSlaves
from Products.PageTemplates.Expressions import getEngine
from Products.PloneFormGen.content.form import FormFolder
from zope.i18n import translate


logger = logging.getLogger('PFGMasterSelect')


class Migration(BrowserView):

    def fix_write_permissions(self):
        from plone.protect.interfaces import IDisableCSRFProtection
        from zope.interface import alsoProvides
        alsoProvides(self.request, IDisableCSRFProtection)

        catalog = self.context.portal_catalog

        for brain in catalog(portal_type=('FormMasterSelectStringField', 'FormMasterMultiSelectStringField',)):
            obj = brain.getObject()

            from Products.CMFCore.permissions import View
            obj.fgField.write_permission = View
            obj._p_changed = True

            logger.warning('Fixed write permission of object %s' % '/'.join(obj.getPhysicalPath()))

    def migrate_to_v02(self):
        from plone.protect.interfaces import IDisableCSRFProtection
        from zope.interface import alsoProvides
        alsoProvides(self.request, IDisableCSRFProtection)

        catalog = self.context.portal_catalog

        for brain in catalog(portal_type=('FormMasterSelectStringField', 'FormMasterMultiSelectStringField',)):
            obj = brain.getObject()

            logger.warning('Updating slave field configuration of object %s' % '/'.join(obj.getPhysicalPath()))

            slave_fields = obj.getSlave_fields()
            obj.setSlave_fields(slave_fields)
            obj._p_changed = True


class SetupSlaves(SetupSlaves):
    pass


class JSONValuesForAction(JSONValuesForAction):

    def evaluate_method(self, method, args):
        assert method
        assert isinstance(method, Expression.Expression)

        # Assumptions:
        # There are two possibilities: This is called on a (a) single select field or (b) multi select field.
        # In case (a) there should always be exactly one value, hence len(args) == 1, and it should not be a
        # dictionary. On the other hand in case (b) there can be an arbitrary count of elements selected and all
        # elements are stored in dictionaries.
        if len(args) == 0 or isinstance(args[0], dict):
            data = dict(values=[str(arg['val']) for arg in args if arg['selected']])
        else:
            assert len(args) == 1
            data = dict(value=str(args[0]))

        econtext = getEngine().getContext(data)

        try:
            result = method(econtext)
        except Exception as e:
            logger.error('%s for "%s %s" of %s/%s crashed: %s',
                         'vocab_method' if self.action in ('vocabulary', 'value') else 'toggle_method',
                         self.action,
                         self.slaveid,
                         '/'.join(self.context.getPhysicalPath()),
                         self.field,
                         e)
            result = None
        return result

    def getSlaves(self, fieldname):
        #assert isinstance(self.context, FormFolder)

        field_object = self.context.findFieldObjectByName(fieldname)
        slave_fields = field_object.fgField.widget.slave_fields or ()
        return slave_fields

    def __call__(self):
        #assert isinstance(aq_base(self.context), FormFolder)
        return Products.MasterSelectWidget.browser.JSONValuesForAction.__call__(self)


class JSONValuesForVocabularyChange(JSONValuesForAction):

    def computeJSONValues(self, slave, args):
        method = slave['vocab_method']
        vocabulary = self.evaluate_method(method, args) if method else ()
        if not isinstance(vocabulary, (list, tuple,)):
            vocabulary = (vocabulary,)
        vocabulary = [str(item) for item in vocabulary]
        vocabulary = DisplayList(zip(vocabulary, vocabulary))

        return json.dumps([
                dict(
                    value=item,
                    label=translate(vocabulary.getValue(item), context=self.request)
                ) for item in vocabulary
            ])


class JSONValuesForValueUpdate(JSONValuesForAction):

    def computeJSONValues(self, slave, args):
        method = slave['vocab_method']
        value = self.evaluate_method(method, args) if method else None
        return json.dumps(translate(value, context=self.request))


class JSONValuesForToggle(JSONValuesForAction):

    def computeJSONValues(self, slave, args):
        method = slave['toggle_method']
        if method:
            toggle = self.evaluate_method(method, args)
        else:
            hide_values = slave.get('hide_values')
            hide_values = [s.strip() for s in hide_values.split(',')]
            toggle = str(args[0]) in hide_values

        action = self.action
        if action in ['disable', 'hide']:
            toggle = not toggle
            action = action == 'disable' and 'enable' or 'show'
        json_toggle = json.dumps({'toggle': toggle, 'action': action})

        return json_toggle
