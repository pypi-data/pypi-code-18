# -*- coding: utf-8 -*-
from typing import Any
from functools import wraps
from flask import current_app, abort
from .utils import username_from_request
from .model import Group


class DecoratorContext(dict):
    """A specialized dict, used in request decorators.  The keys are accessible
    using normal dict style or with attribute (dot) style syntax.

    """

    def __getattr__(self, key: str) -> Any:
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value


def _pass_open_directory(fn):
    """Helper to pass the open_directory registered with the current application
    into a decorator function.


    """
    @wraps(fn)
    def decorator(*args, **kwargs):
        od = getattr(current_app, 'extensions', {}).get('open_directory')
        if od is None:
            raise TypeError()
        return fn(od, *args, **kwargs)
    return decorator


def pass_context(fn):
    """Helper that passes a :class:`DecoratorContex` with the
    :class:`OpenDirectory` registered with the current application and the
    ``username`` for the request.  This will pass the ``context`` as the first
    arg to the decorator.

    .. seealso:: :ref:`custom_decorators`

    """
    @wraps(fn)
    @_pass_open_directory
    def decorator(open_directory, *args, **kwargs):
        ctx = DecoratorContext(
            open_directory=open_directory,
            username=username_from_request()
        )
        return fn(ctx, *args, **kwargs)
    return decorator


def requires_group(group_name):
    """Decorator to mark a flask route as requiring the authenticated user
    to be apart of the specified group.

    :param group_name:  The group name to query the open_directory
                        connection for and is required that the username
                        (retrieved from ``Authorization`` header in the
                        request) is apart of the given group.  If the
                        user is not then we abort with a ``401`` code.

    Example::

        # app.py
        from flask import Flask
        from open_directory_utils import OpenDirectory, utils, requires_group

        app = Flask(__name__)
        app.config['OPEN_DIRECTORY_SERVER'] = 'example.com'

        od = OpenDirectory(app)

        ... other routes

        @app.route('/admins')
        @requires_group('administrators')
        def admins_only():
            return "Hello, '{}'. You are an administrator".format(
                utils.username_from_request()
            )


    """
    def inner(fn):

        @wraps(fn)
        @pass_context
        def decorator(ctx, *args, **kwargs):
            od, username = ctx['open_directory'], ctx['username']
            if username is not None:
                group = od.query(Group).filter(group_name=group_name).first()
                if group and group.has_user(username):
                    return fn(*args, **kwargs)
                return abort(401)
        return decorator
    return inner


def _requires_groups(*group_names, _all=True):
    """Helper for ``requires_all_groups`` and ``requires_any_group`` decorators.

    """
    if _all is True:
        test_fn = all
    else:
        test_fn = any

    def inner(fn):

        @wraps(fn)
        @pass_context
        def decorator(ctx, *args, **kwargs):
            od, username = ctx['open_directory'], ctx['username']
            groups = [od.query(Group).filter(group_name=g).first() for g in
                      group_names]
            if test_fn(map(lambda g: g.has_user(username), groups)):
                return fn(*args, **kwargs)
            return abort(401)
        return decorator
    return inner


def requires_all_groups(*group_names):
    """Decorator to mark a flask route as requiring the authenticated user
    to be apart of all the passed in groups.

    This is similar to the ``requires_group``, only it accepts multiple
    groups to check against.

    :param group_names:  The group name(s) to query the open_directory
                         connection for and is required that the username
                         (retrieved from ``Authorization`` header in the
                         request) is apart of the given group.  If the
                         user is not then we abort with a ``401`` code.

    Example::

        # app.py
        from flask import Flask
        from open_directory_utils import OpenDirectory, utils, \
            requires_all_groups

        app = Flask(__name__)
        app.config['OPEN_DIRECTORY_SERVER'] = 'example.com'

        open_directory = OpenDirectory(app)


        @app.route('/office-admins')
        @requires_all_groups('administrators', 'office')
        def office_admins():
            return "Hello, '{}'. You are an office administrator".format(
                utils.username_from_request()
            )

    """
    return _requires_groups(*group_names, _all=True)


def requires_any_group(*group_names):
    """Decorator to mark a flask route as requiring the authenticated user
    to be apart of any of the passed in groups.

    This is similar to the ``requires_all_groups``, only it accepts multiple
    groups to check against, and succeeds if the authenticated user is a member
    of any of the specified groups.

    :param group_names:  The group name(s) to query the open_directory
                         connection for and is required that the username
                         (retrieved from ``Authorization`` header in the
                         request) is apart of the given group.  If the
                         user is not then we abort with a ``401`` code.

    Example::

        # app.py
        from flask import Flask
        from open_directory_utils import OpenDirectory, utils, \
            requires_any_group

        app = Flask(__name__)
        app.config['OPEN_DIRECTORY_SERVER'] = 'example.com'

        open_directory = OpenDirectory(app)

        @app.route('/office-or-admins')
        @requires_any_group('administrators', 'office')
        def office_or_admins():
            return "Hello, '{}'. You're an administrator or office user".format(
                utils.username_from_request()
            )


    """
    return _requires_groups(*group_names, _all=False)
