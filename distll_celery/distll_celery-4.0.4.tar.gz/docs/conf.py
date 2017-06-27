# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from sphinx_celery import conf

globals().update(conf.build_config(
    'distll_celery', __file__,
    project='Celery',
    version_dev='5.0',
    version_stable='4.0',
    canonical_url='http://docs.celeryproject.org',
    webdomain='celeryproject.org',
    github_project='distll_celery/distll_celery',
    author='Ask Solem & contributors',
    author_name='Ask Solem',
    copyright='2009-2016',
    publisher='Celery Project',
    html_logo='images/celery_512.png',
    html_favicon='images/favicon.ico',
    html_prepend_sidebars=['sidebardonations.html'],
    extra_extensions=[
        'sphinx.ext.napoleon',
        'distll_celery.contrib.sphinx',
        'celerydocs',
    ],
    extra_intersphinx_mapping={
        'cyanide': ('https://cyanide.readthedocs.io/en/latest', None),
    },
    apicheck_ignore_modules=[
        'distll_celery.five',
        'distll_celery.__main__',
        'distll_celery.task',
        'distll_celery.contrib.testing',
        'distll_celery.contrib.testing.tasks',
        'distll_celery.task.base',
        'distll_celery.bin',
        'distll_celery.bin.celeryd_detach',
        'distll_celery.contrib',
        r'distll_celery.fixups.*',
        'distll_celery.local',
        'distll_celery.app.base',
        'distll_celery.apps',
        'distll_celery.canvas',
        'distll_celery.concurrency.asynpool',
        'distll_celery.utils.encoding',
        r'distll_celery.utils.static.*',
    ],
))

settings = {}
ignored_settings = {
    # Deprecated broker settings (replaced by broker_url)
    'broker_host',
    'broker_user',
    'broker_password',
    'broker_vhost',
    'broker_port',
    'broker_transport',

    # deprecated task settings.
    'chord_propagates',

    # MongoDB settings replaced by URL config.,
    'mongodb_backend_settings',

    # Database URL replaced by URL config (result_backend = db+...).
    'database_url',

    # Redis settings replaced by URL config.
    'redis_host',
    'redis_port',
    'redis_db',
    'redis_password',

    # Old deprecated AMQP result backend.
    'result_exchange',
    'result_exchange_type',

    # Experimental
    'worker_agent',

    # Deprecated worker settings.
    'worker_pool_putlocks',
}


def configcheck_project_settings():
    from distll_celery.app.defaults import NAMESPACES, flatten
    settings.update(dict(flatten(NAMESPACES)))
    return set(settings)


def is_deprecated_setting(setting):
    try:
        return settings[setting].deprecate_by
    except KeyError:
        pass


def configcheck_should_ignore(setting):
    return setting in ignored_settings or is_deprecated_setting(setting)
