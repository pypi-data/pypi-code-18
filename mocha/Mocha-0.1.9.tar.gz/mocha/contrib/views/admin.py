"""
views.admin is a basic home page for your admin area
"""

from mocha import (Mocha,
                   utils,
                   decorators as deco,
                   )

import mocha.contrib

__options__ = utils.dict_dot({})


@mocha.contrib.admin
class Admin(Mocha):

    @classmethod
    def _register(cls, app, **kwargs):

        # Route
        kwargs["base_route"] = __options__.get("route", "/admin/")

        super(cls, cls)._register(app, **kwargs)

    @deco.template("contrib/admin/Admin/index.jade")
    @deco.nav_title("Admin Home", tags=mocha.contrib.ADMIN_TAG, attach_to=["mocha.contrib.views.auth.Account", "self"])
    def index(self):
        return
