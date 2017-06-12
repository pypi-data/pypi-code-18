""".. Ignore pydocstyle D400.

===================
Frontend decorators
===================

.. autofunction:: rolca.frontend.decorators.check_contest_login_required

"""
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from rolca.core.models import Contest


def check_contest_login_required(function):
    """Use ``login_required`` decorator if contest has set ``login_required``."""
    @wraps(function)
    def decorator(*args, **kwargs):  # pylint: disable=missing-docstring
        contest_id = kwargs.get('contest_id')
        contest = get_object_or_404(Contest, pk=contest_id)

        if contest.login_required:
            return login_required(function)(*args, **kwargs)

        return function(*args, **kwargs)

    return decorator
