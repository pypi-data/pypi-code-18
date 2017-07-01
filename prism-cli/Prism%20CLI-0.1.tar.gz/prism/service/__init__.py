#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

from .. import log


def get_service(app):
    try:
        mod = __import__('prism.service.%s' % app.app_config['service'], globals(), locals(), ['object'], 0)
        return mod
    except:
        log.die('Service %r failure.' % app.app_config['service'])

def depends(app, args):
    return get_service(app).depends(app, args)

def create(app, args):
    return get_service(app).create(app, args)

def destroy(app, args):
    return get_service(app).destroy(app, args)

def start(app, args):
    return get_service(app).start(app, args)

def stop(app, args):
    return get_service(app).stop(app, args)
