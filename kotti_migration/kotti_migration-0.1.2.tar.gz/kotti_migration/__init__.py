# -*- coding: utf-8 -*-

"""
Created on 2017-05-22
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from kotti.resources import File
from pyramid.i18n import TranslationStringFactory
from kotti_migration import config as km_config

_ = TranslationStringFactory('kotti_migration')


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_migration.kotti_configure

        to enable the ``kotti_migration`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_migration'
    settings['kotti.fanstatic.view_needed'] += ' kotti_migration.fanstatic.css_and_js'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """
    config.add_static_view('static-kotti_migration', 'kotti_migration:static')

    m_ignores = config.registry.settings.get("migration.ignore_content_types", "")
    km_config.ignore_content_types = m_ignores.split("\n")


    config.scan(__name__)
