#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

import os
import json
import shutil

from . import log
from . import command
from .command import Package, Library

from . import exposer


class Static:
    default_main_config = {'apps': {}}
    default_app_config = {'config': {}, 'locations': []}

    main = '/etc/prism/'
    env = os.path.join(main, 'env/')
    config = os.path.join(main, 'config.json')

    services = '/etc/systemd/system/'

config = None

def verify_dependencies():
    if command.exists('apt'):
        Package.is_yum = False
        log.die('No apt support, yet!')
    elif command.exists('yum'):
        def pkg_install(pkg):
            if command.exists('sudo'):
                command.run('yum install -y %s' % pkg, use_splitter=True)
            else:
                command.run('sudo yum install -y %s' % pkg, use_splitter=True)

        Package.install = pkg_install
    else:
        log.die('Package manager not supported!')

    Package.require('python-devel', apt='python-dev')
    Library.require('virtualenv')

    if 'enabled' not in command.get_output_quiet('systemctl is-enabled nginx'):
        log.info('Enabling and Starting Nginx')
        command.run('systemctl enable nginx')
        command.run('systemctl start nginx')

    if not os.path.exists(Static.main):
        log.action('Created %r' % Static.main)
        os.mkdir(Static.main)

    if not os.path.exists(Static.env):
        log.action('Created %r' % Static.env)
        os.mkdir(Static.env)

def verify_structure():
    if not os.path.exists(Static.main):
        log.action('Created %r' % Static.main)
        os.mkdir(Static.main)

    if not os.path.exists(Static.config):
        log.action('Created %r' % Static.config)

        with open(Static.config, 'w') as file:
            json.dump(Static.default_main_config, file)

def load_config():
    with open(Static.config) as file:
        global config
        config = json.load(file)

def save_config():
    with open(Static.config, 'w') as file:
        json.dump(config, file)

def nuke():
    log.header('Prism Nuke in Progress')
    from prism import App
    import prism.action.destroy
    apps = config['apps'].copy()
    for app in apps:
        log.header('Application %r is About to be Nuked' % app)
        prism.action.destroy.run(App(app), None)

    command.run('rm -rf %s' % Static.main)
    log.die('Prism nuked')

verify_dependencies()
verify_structure()
load_config()
