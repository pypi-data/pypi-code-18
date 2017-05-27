# -*- coding: utf-8 -*-
import os

from flask import _app_ctx_stack

from .query import Query
from .base import BaseOpenDirectory


# CONFIGURATION
OPEN_DIRECTORY_SERVER = os.environ.get('OPEN_DIRECTORY_SERVER', 'localhost')
OPEN_DIRECTORY_BASE_DN = os.environ.get('OPEN_DIRECTORY_BASE_DN', None)


class OpenDirectory(BaseOpenDirectory):

    def __init__(self, app=None):
        config = {
            'OPEN_DIRECTORY_SERVER': OPEN_DIRECTORY_SERVER,
            'OPEN_DIRECTORY_BASE_DN': OPEN_DIRECTORY_BASE_DN,
        }
        super().__init__(**config)

        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the extension with the application.

        :param app: The :class:`flask.Flask` application to register the
                    extension with.

        """
        self.config.update(app.config)

        if not hasattr(app, 'extensions'):
            app.extensions = {}  # pragma: no cover

        app.extensions['open_directory'] = self

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)  # pragma: no cover

    def teardown(self, exception):
        """Clean-up for the extension.

        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if hasattr(ctx, 'open_directory_connection'):
                ctx.open_directory_connection.unbind()
                del(ctx.open_directory_connection)

    def query(self, model=None, **kwargs) -> Query:
        """Create a query with this instance as it's ``open_directory``
        attribute.

        :param model:  An optional :class:`ModelABC` subclass to set for the
                       query.

        :param kwargs:  Extra key-word arguments to pass to the :class:`Query`,
                        constructor.

        """
        kwargs['open_directory'] = self
        kwargs['model'] = model
        return Query(**kwargs)
