#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

import os

from ..deco import header, require_app, log_group
from .. import log
from ..config import Static, save_config
from ..config import config as prism_config
from .. import command

from .. import service
from .. import exposer

from .stop import run as action_stop


@header('App Destruction')
@require_app
@log_group('Destroying application...', 'Application destroyed')
def run(app, args):
    # Stop the service
    action_stop(app, args)

    # Destroy the service files
    service.destroy(app, args)

    if app.has_exposer:
        # Tell the exposer to destroy the app config
        exposer.destroy(app, args)

    # Remove the app environment
    command.run('rm -rf %s' % app.app_env)

    # Remove the app from the config
    del prism_config['apps'][app.app_name]
    save_config()
