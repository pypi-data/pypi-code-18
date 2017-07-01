#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

import os

from ..deco import header, require_app
from .. import log

from .restart import run as action_restart
from .stop import run as action_stop

from .. import exposer
from .. import service


@header('App WWW Exposer')
@require_app
def run(app, args):
    if not app.has_exposer:
        log.fail('Application has no exposer set!')
        return

    if 'routes' not in app.config:
        log.fail('No routes set. Nothing to change!')
        return

    if 'exposed' not in app.app_config:
        app.app_config['exposed'] = False
        app.save_config()

    if args.action == 'expose':
        app.app_config['exposed'] = not app.app_config['exposed']
        app.save_config()
    elif 'exposed' not in app.app_config or not app.app_config['exposed']:
        log.fail('Application not exposed. To expose your app through %r, run: prism expose' % app.app_config['service'])
        return

    if app.app_config['exposed']:
        log.doing('Exposing application via %r...' % app.app_config['service'])

        # Create the exposer config files
        exposer.create(app, args)

        # Restart the service
        action_restart(app, args)

        log.action('Config generated for %r, application exposed successfully' % app.app_config['service'])
    else:
        log.doing('Unexposing application via %r...' % app.app_config['service'])

        # Destroy the exposer config
        exposer.destroy(app, args)

        # Stop the service
        action_stop(app, args)

        log.fail('Application no longer exposed. Run the command again to re-expose the application')
