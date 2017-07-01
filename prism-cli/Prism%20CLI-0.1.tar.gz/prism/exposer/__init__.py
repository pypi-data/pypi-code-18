#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

from .. import log


def get_exposer(app):
    try:
        mod = __import__('prism.exposer.%s' % app.app_config['exposer'], globals(), locals(), ['object'], 0)
        return mod
    except:
        log.die('Exposer %r failure.' % app.app_config['exposer'])

def depends(app, args):
    get_exposer(app).depends(app, args)

def create(app, args):
    get_exposer(app).create(app, args)

    # If a file was created, it makes sense to restart the service
    restart(app, args)

def destroy(app, args):
    get_exposer(app).destroy(app, args)

    # If a file was destroyed, it makes sense to restart the service
    restart(app, args)

def restart(app, args):
    get_exposer(app).restart(app, args)
