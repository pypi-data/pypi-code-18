#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

import os
import shutil

from ..deco import header, require_app, log_group
from .. import log
from .. import protocol
from .. import template

from .depends import run as action_depends


@header('App Updating')
@require_app
@log_group('Building application files...', 'Application tree generated')
def run(app, args):
    if os.path.exists(app.app_folder):
        app.command.run('rm -rf %s' % app.app_folder)

    if os.path.exists(os.path.join(app.app_env, 'wsgi.py')):
        app.command.run('rm -rf %s' % os.path.join(app.app_folder, 'wsgi.py'))

    # Rebuild the app environment
    protocol.build(app, args)

    # Install dependencies
    action_depends(app, args)

    # If there is a wsgi file, copy that to the environment base directory.
    if os.path.exists(os.path.join(app.app_folder, 'wsgi.py')):
        log.info('Using \'wsgi.py\' in application files')
        shutil.copyfile(os.path.join(app.app_folder, 'wsgi.py'), os.path.join(app.app_env, 'wsgi.py'))
    else:
        # If there is no wsgi file, generate one.
        log.info('File not found. Generating \'wsgi.py\'')
        with open(os.path.join(app.app_env, 'wsgi.py'), 'w') as file:
            file.write(template.get('wsgi', {'app_name': os.path.basename(app.app_folder)}))

    # If there is no __init__.py, create one so it's recognized as a module
    if not os.path.exists(os.path.join(app.app_folder, '__init__.py')):
        log.info('Generating \'__init__.py\' in application files')
        open(os.path.join(app.app_folder, '__init__.py'), 'a').close()
