#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

def create(app, args):
    app.app_config['type'] = 'file'
    return args.file

def build(app, args):
    app.command.run('cp -R %s %s' % (app.app_config['source_folder'], app.app_env))
