#
# Flask-SRI
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import json
import warnings


class SRI(object):
    """
    Flask-SRI

    Documentation:
    https://flask-sri.readthedocs.io

    For use with the Grunt SRI plug-in:
    https://github.com/neftaly/grunt-sri

    :param app: Flask app to initialize with. Defaults to `None`
    """

    sri_directives = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        try:
            with app.open_resource(app.config.get('SRI_DIRECTIVES'), mode='r') as f:
                self.sri_directives = json.load(f)
        except IOError:
            warnings.warn('SRI_DIRECTIVES not set', RuntimeWarning, stacklevel=2)
            self.sri_directives = {}
        app.jinja_env.globals.update(sri=self.sri)

    def sri(self, resource):
        return self.sri_directives.get('@' + resource, '')


# EOF
