# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

from plone import api

from . import TYPE_CONFIG


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'collective.behavior.internalnumber:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    api.portal.set_registry_record(TYPE_CONFIG, [])


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
