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

from .. import exposer
from .. import service


@header('App Depends Install')
@require_app
@log_group('Installing requirements...', 'Requirements installed')
def run(app, args):
    if app.has_exposer:
        # Install exposer dependencies
        exposer.depends(app, args)

    # Install service dependencies
    service.depends(app, args)

    # Install python requirements
    if os.path.exists(os.path.join(app.app_folder, 'requirements.txt')):
        app.command.run_in_virtualenv('pip install -r requirements.txt', precmd=['cd ' + app.app_name], use_splitter=True)
    else:
        log.info('No requirements.txt, skipping dependency install')
