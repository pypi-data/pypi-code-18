# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from zope.interface import Interface, Attribute
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveWfadaptationsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IWorkflowAdaptation(Interface):

    """Interface for workflow adaptations."""

    schema = Attribute("""Associated schema that provides parameters for the
        workflow adaptation""")

    def patch_workflow(self, workflow_name, *parameters):
        """Patch the workflow.

        :param workflow_name: [required] name of the workflow
        :type workflow_name: Unicode object

        :param parameters: [required] the parameters needed for the adaptation
        :type parameters: dict

        :returns: (success, message) where success is a boolean and an
        additional message that describes the success or the failure.
        :rtype: (bool, str)
        """
        pass
