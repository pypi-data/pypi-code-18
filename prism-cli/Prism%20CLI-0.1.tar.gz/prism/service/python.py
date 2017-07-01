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


def depends(app, args):
    pass

def create(app, args):
    with open(os.path.join(Static.services, 'prism_%s.service' % app.app_name), 'w') as file:
        file.write(template.get('service-python', {'app_name': app.app_name, 'app_env': app.app_env}))
    command.run('systemctl daemon-reload')

def destroy(app, args):
    if os.path.exists(os.path.join(Static.services, 'prism_%s.service' % app.app_name)):
        stop(app, args)

        command.run('rm -f %s' % os.path.join(Static.services, 'prism_%s.service' % app.app_name))
        command.run('systemctl daemon-reload')

def start(app, args):
    if 'enabled' not in command.get_output_quiet('systemctl is-enabled prism_%s' % app.app_name):
        command.run('systemctl enable prism_%s' % app.app_name)
    if 'active' not in command.get_output_quiet('systemctl is-active prism_%s' % app.app_name):
        command.run('systemctl start prism_%s' % app.app_name)

def stop(app, args):
    if 'inactive' not in command.get_output_quiet('systemctl is-active prism_%s' % app.app_name):
        command.run('systemctl stop prism_%s' % app.app_name)
    if 'disabled' not in command.get_output_quiet('systemctl is-enabled prism_%s' % app.app_name):
        command.run('systemctl disable prism_%s' % app.app_name)
