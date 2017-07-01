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
from .. import protocol
from .. import App

from .update import run as action_update


@header('App Creation')
@require_app(inverse=True)
@log_group('Creating application...', 'Application created')
def run(app, args):
    command.run('virtualenv %s' % app.app_name, use_splitter=True)

    prism_config['apps'][app.app_name] = Static.default_app_config
    app.app_config = prism_config['apps'][app.app_name]


    if args.file:
        app.app_config['type'] = 'file'
    elif args.git:
        app.app_config['type'] = 'git'

    if 'service' in app.app_config and app.app_config['service'] != args.service:
        log.fail('Service specified, but a service is already set in the config! Defaulting to existing config value!')
    else:
        app.app_config['service'] = args.service
    log.info('Using service %r' % app.app_config['service'])

    if 'exposer' in app.app_config and app.app_config['exposer'] != args.service:
        log.fail('Exposer specified, but an exposer is already set in the config! Defaulting to existing config value!')
    else:
        app.app_config['exposer'] = args.exposer
    if app.has_exposer:
        log.info('Using exposer %r' % app.app_config['exposer'])
    else:
        log.info('No exposer defined')


    app.app_config['source_folder'] = protocol.create(app, args)

    app.app_config['locations'].append(app.app_env)
    app.app_config['locations'].append(app.app_config['source_folder'])

    if args.local_config or os.path.exists(os.path.join(app.app_config['source_folder'], 'prism.json')):
        if not args.local_config:
            log.fail('Local config option not set, but a config exists in the source directory! Defaulting to existing local config!')
        app.app_config['config'] = 'local'

    save_config()

    app = App(app.app_name)

    action_update(app, args)

    app.save_config()
