# -*- coding: utf-8 -*-
"""Example."""
from zope import schema
from zope.interface import Interface

from plone import api

from collective.wfadaptations.wfadaptation import WorkflowAdaptationBase


class IExampleParameters(Interface):

    state_name = schema.TextLine(
        title=u"State name",
        required=True)

    new_state_title = schema.TextLine(
        title=u"New state title",
        required=True)


class ExampleWorkflowAdaptation(WorkflowAdaptationBase):

    """Example workflow adaptation that change a state title."""

    schema = IExampleParameters

    def patch_workflow(self, workflow_name, **parameters):
        """Change a state title."""
        wtool = api.portal.get_tool('portal_workflow')
        workflow = wtool[workflow_name]
        state_name = parameters['state_name']
        msg = self.check_state_in_workflow(workflow, state_name)
        if msg:
            return False, msg

        state = workflow.states[state_name]
        new_title = parameters['new_state_title']
        if state.title == new_title:
            message = "The state title was already '{}'.".format(new_title)
            return False, message

        state.setProperties(
            title=new_title,
            description=state.description,
            transitions=list(state.transitions))
        message = "The state title has been successfully changed."
        return True, message
