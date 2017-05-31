# -*- coding: utf-8 -*-
"""Views to manage workflow adaptations."""
from zope import schema
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory

from Products.Five import BrowserView
from plone import api
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.form import Form
from z3c.form.field import Fields

from collective.wfadaptations import _
from collective.wfadaptations.api import add_applied_adaptation
from collective.wfadaptations.api import get_applied_adaptations
from collective.wfadaptations.api import get_applied_adaptations_for_workflow
from collective.wfadaptations.interfaces import IWorkflowAdaptation


PMF = MessageFactory("plone")


class IAssociateWorkflowAdaptation(model.Schema):

    """View to associate workflow adaptations to workflows."""

    workflow = schema.Choice(
        title=_(u'Workflow'),
        vocabulary="plone.app.vocabularies.Workflows"
    )

    adaptation = schema.Choice(
        title=_(u'Workflow adaptation'),
        description=_(u'Workflow adaptation to execute on this workflow'),
        vocabulary="collective.wfadaptations.WorkflowAdaptations"
    )


class AssociateWorkflowAdaptationForm(Form):

    """Associate an adaptation to a workflow, step 1."""

    label = _(u"Associate an adaptation to a workflow")
    fields = Fields(IAssociateWorkflowAdaptation)
    ignoreContext = True

    @button.buttonAndHandler(PMF(u'Next'), name='next')
    def handleNext(self, action):
        """Handle add action."""
        pass  # we never come here

    @button.buttonAndHandler(PMF('label_cancel', default=u'Cancel'),
                             name='cancel')
    def handleCancel(self, action):
        """Cancel."""
        super(AssociateWorkflowAdaptationForm, self).handleCancel(action)

    def updateActions(self):
        super(AssociateWorkflowAdaptationForm, self).updateActions()
        if 'send' in self.actions:
            self.actions["next"].addClass("context")

        if 'cancel' in self.actions:
            self.actions["cancel"].addClass("standalone")


class ParametersForm(Form):

    """Choose parameters for the workflow adaptation."""

    label = _(u"Choose parameters for your workflow adaptation")
    ignoreContext = True

    def __init__(self, context, request):
        super(ParametersForm, self).__init__(context, request)
        self.workflow = request.get('form.widgets.workflow')[0]
        self.adaptation_name = request.get('form.widgets.adaptation')[0]

    @property
    def fields(self):
        fields = Fields(IAssociateWorkflowAdaptation)
        for field_name in fields:
            fields[field_name].mode = HIDDEN_MODE

        adaptation = getUtility(IWorkflowAdaptation, self.adaptation_name)
        if adaptation.schema:
            fields += Fields(adaptation.schema)
        return fields

    @button.buttonAndHandler(PMF(u'Save'), name='save')
    def handleApply(self, action):
        """Apply the workflow adaptation."""
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        adaptation = data.pop('adaptation')
        workflow_name = data.pop('workflow')

        message_type = 'error'
        message = _(
            "The workflow adaptation has not been successfully applied.")
        already_applied = get_applied_adaptations_for_workflow(workflow_name)
        adaptation_name = self.request['form.widgets.adaptation'][0]

        # An adaptation can not be applied more than once on a workflow
        if adaptation_name in already_applied:
            additional_message = _(
                "This adaptation is already applied on this workflow.")
        else:
            success, additional_message = adaptation.patch_workflow(
                workflow_name, **data)
            if success:
                add_applied_adaptation(adaptation_name, workflow_name, **data)
                message_type = 'info'
                message = _(
                    "The workflow adaptation has been successfully applied.")

        if additional_message:
            message = _("${message} ${additional}",
                        mapping={'message': message,
                                 'additional': additional_message})

        api.portal.show_message(message, self.request, message_type)
        portal_url = api.portal.get().absolute_url()
        self.request.response.redirect(
            "{}/@@manage_workflow_adaptations".format(portal_url))

    @button.buttonAndHandler(PMF('label_cancel', default=u'Cancel'),
                             name='cancel')
    def handleCancel(self, action):
        """Cancel."""
        portal_url = api.portal.get().absolute_url()
        self.request.response.redirect(
            "{}/@@manage_workflow_adaptations".format(portal_url))

    def updateActions(self):
        super(ParametersForm, self).updateActions()
        if 'send' in self.actions:
            self.actions["save"].addClass("context")

        if 'cancel' in self.actions:
            self.actions["cancel"].addClass("standalone")


class AssociateWorkflowAdaptation(FormWrapper):

    form = AssociateWorkflowAdaptationForm

    def __init__(self, context, request):
        """Determine if we are in step 1 or step 2."""
        params = set(request.keys())
        if 'form.widgets.adaptation' in params:
            self.form = ParametersForm

        super(AssociateWorkflowAdaptation, self).__init__(context, request)


class ListWorkflowAdaptations(BrowserView):

    """View that lists applied workflow adaptations."""

    def adaptations(self):
        """Return applied adaptations."""
        return get_applied_adaptations()
