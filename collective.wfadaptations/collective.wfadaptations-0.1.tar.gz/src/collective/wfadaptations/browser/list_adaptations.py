# -*- coding: utf-8 -*-
"""List workflow adaptations."""
from Products.Five import BrowserView

from collective.wfadaptations.api import get_applied_adaptations


class ListWorkflowAdaptations(BrowserView):

    """View that lists applied workflow adaptations."""

    def adaptations(self):
        """Return applied adaptations."""
        return get_applied_adaptations()
