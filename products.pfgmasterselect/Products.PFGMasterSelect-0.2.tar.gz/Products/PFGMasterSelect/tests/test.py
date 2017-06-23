import unittest

from Products.CMFCore import Expression
from Products.PFGMasterSelect.browser import JSONValuesForAction
from mock import MagicMock, ANY
from plone.testing.z2 import Browser

import transaction
from Products.PFGMasterSelect.testing import MASTER_SELECT_FUNCTIONAL_TESTING, MASTER_SELECT_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles



class TestJSONValuesForAction(unittest.TestCase):

    layer = MASTER_SELECT_INTEGRATION_TESTING

    def setUp(self):
        self.context = MagicMock()
        self.context.findFieldObjectByName.return_value = None
        self.context.provides.return_value = True
        self.request = MagicMock(field=None, slave=None, value=None, action=None)
        self.obj = JSONValuesForAction(self.context, self.request)

    def tearDown(self):
        del self.context
        del self.request
        del self.obj

    def test_getSlaves_none_fieldname(self):
        with self.assertRaises(AttributeError):
            self.obj.getSlaves(None)

    def test_getSlaves_empty_fieldname(self):
        with self.assertRaises(AttributeError):
            self.obj.getSlaves('')

    def test_getSlaves_unknown_fieldname(self):
        with self.assertRaises(AttributeError):
            self.obj.getSlaves('unknnown')

    def test_getSlaves_known_fieldname(self):
        SLAVE_FIELDS = (1, 2, 3,)
        field_object = MagicMock()
        field_object.fgField.widget.slave_fields = SLAVE_FIELDS
        context = MagicMock()
        context.findFieldObjectByName.return_value = field_object
        request = dict(field=None, slave=None, value=None, action=None)
        obj = JSONValuesForAction(context, request)
        self.assertEquals(SLAVE_FIELDS, obj.getSlaves('known'))

    def test_evaluate_method_none_method(self):
        with self.assertRaises(AssertionError):
            self.obj.evaluate_method(None, [])

    def test_evaluate_method_single(self):
        VALUE = '2'
        expr = Expression.Expression('python: value')
        args = VALUE
        self.assertEquals(VALUE, self.obj.evaluate_method(expr, args))

    def test_evaluate_method_multi(self):
        VALUES_SELECTED = ('1', '2',)
        VALUES_NOT_SELECTED = ('4',)
        expr = Expression.Expression('python: sum(map(int, values))')
        args = [dict(selected=True, val=v) for v in VALUES_SELECTED] \
               + [dict(selected=False, val=v) for v in VALUES_NOT_SELECTED]
        self.assertEquals(3, self.obj.evaluate_method(expr, args))

    def test_argument_format_expectation_single(self):
        self.assertEquals([42], self.obj.extractArguments(None, '42'))

    def test_argument_format_expectation_multi(self):
        self.assertEquals([dict(selected=True, val='3'), dict(selected=False, val='7')],
                          self.obj.extractArguments(None, '[{"selected":true,"val":"3"},{"selected":false, "val":"7"}]'))

    def test_extracted_arguments_passed_directly_to_compute(self):
        SLAVES = [dict(name='a', action='hide')]
        VALUE = '"test43"'
        self.obj.action = 'hide'
        self.obj.value = VALUE
        self.obj.slaveid = SLAVES[0]['name']
        self.obj.getSlaves = MagicMock(return_value=SLAVES)
        self.obj.extractArguments = MagicMock(return_value=VALUE)
        self.obj.computeJSONValues = MagicMock()
        self.obj()

        self.obj.computeJSONValues.assert_called_with(ANY, VALUE)


class Test(unittest.TestCase):

    layer = MASTER_SELECT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.layer['request']

        portal = self.portal

        setRoles(self.portal, TEST_USER_ID, ['Manager',])

        portal.invokeFactory('FormFolder', 'formfolder')
        self.form = portal.formfolder

        self.form.invokeFactory('FormMasterSelectStringField', 'master')
        self.master = self.form.master

        self.form.invokeFactory('FormMasterSelectStringField', 'slave')
        slave = self.form.slave

        self.master.setFgVocabulary(['1', '2'])
        self.master.setSlave_fields([dict(name='slave', action='hide', vocab_method='', toggle_method='value in ("1")', hide_values='2')])

        transaction.commit()

        self.browser = Browser(self.app)
        self.browser.handleErrors = False

    def test(self):
        browser = self.browser
        browser.open(self.form.absolute_url() + '/@@masterselect-jsonvalue-toggle?field=master&slave=slave&action=hide&value=1')
        self.assertTrue('"action": "show"' in browser.contents)
        self.assertTrue('"toggle": false' in browser.contents)
