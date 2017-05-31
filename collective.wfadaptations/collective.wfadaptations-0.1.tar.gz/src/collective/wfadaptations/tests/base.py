# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from zope.interface import implements

from collective.wfadaptations.interfaces import IWorkflowAdaptation


class IDummySchema(Interface):

    param = schema.TextLine(
        title=u"Dummy parameter",
        required=True)


class DummyWorkflowAdaptation(object):

    implements(IWorkflowAdaptation)

    schema = IDummySchema

    def patch_workflow(self, workflow_name, **parameters):
        self.patched = "{};{}".format(workflow_name, parameters['param'])
        return True, ''


class AnotherWorkflowAdaptation(object):

    implements(IWorkflowAdaptation)

    schema = None

    def patch_workflow(self, workflow_name, **parameters):
        return True, ''
