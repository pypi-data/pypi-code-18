""".. Ignore pydocstyle D400.

===========================
Frontend context processors
===========================

.. autofunction:: rolca.frontend.context_processors.ui_configuration

"""

from rolca.frontend import settings as rolca_settings


def ui_configuration(request):
    """Set parameters for configuring UI."""
    return {
        'materialize_color': rolca_settings.frontend_color,
        'frontend_title': rolca_settings.frontend_title,
    }
