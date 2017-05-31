# -*- coding: utf-8 -*-

from zope.interface import implements
from collective.wfadaptations.interfaces import IWorkflowAdaptation

from . import _


class WorkflowAdaptationBase(object):

    implements(IWorkflowAdaptation)

    schema = None

    def check_state_in_workflow(self, workflow, state_name):
        """ Check if state_name is a workflow state"""
        if state_name not in workflow.states:
            message = _("The workflow id '${id}' (${title}) doesn't contain the state '${state}'.",
                        mapping={'id': workflow.id, 'title': workflow.title, 'state': state_name})
            return message
        else:
            return ''

    def check_transition_in_workflow(self, workflow, transition_name):
        """ Check if transition_name is a workflow transition """
        if transition_name not in workflow.transitions:
            message = _("The workflow id '${id}' (${title}) doesn't contain the transition '${transition}'.",
                        mapping={'id': workflow.id, 'title': workflow.title, 'transition': transition_name})
            return message
        else:
            return ''

    def grant_permission(state, perm, role):
        '''For a given p_state, this function ensures that p_role is among roles
           who are granted p_perm.'''
        # to be improved by giving a list of roles
        roles = state.permission_roles[perm]
        if role not in roles:
            roles = list(roles)
            roles.append(role)
            state.setPermission(perm, 0, roles)
