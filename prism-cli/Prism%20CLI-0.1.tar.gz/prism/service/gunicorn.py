#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

import os

from ..config import Static
from .. import command
from .. import template

from . import python


def depends(app, args):
    app.command.run_in_virtualenv('pip install gunicorn', use_splitter=True)

def create(app, args):
    with open(os.path.join(Static.services, 'prism_%s.service' % app.app_name), 'w') as file:
        file.write(template.get('service-gunicorn', {'app_name': app.app_name, 'app_env': app.app_env, 'environment': '', 'workers': 3}))

def destroy(app, args):
    python.destroy(app, args)

def start(app, args):
    python.start(app, args)

def stop(app, args):
    python.stop(app, args)
