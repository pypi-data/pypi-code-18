#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

from ..deco import header, require_app, save_app
from .. import log


@header('App Route')
@require_app
@save_app
def run(app, args):
    if args.do is None:
        if 'routes' not in app.config or len(app.config['routes']) == 0:
            log.die('No routes created. Go ahead and add some!')
        log.header('Routes')
        for i in range(0, len(app.config['routes'])):
            route = app.config['routes'][i]
            s = route['fqdn']

            if 'https' in route and route['https']:
                s = 'https://' + s
            else:
                s = 'http://' + s

            if 'port' in route:
                if route['port'] == 443 and ('https' in route and route['https']):
                    pass
                elif route['port'] == 80 and not ('https' in route and route['https']):
                    pass
                else:
                    s += ':%d' % route['port']

            print('%d: %s' % (i + 1, s))
        return

    if args.do == 'add':
        log.doing('Creating route...')
        if 'routes' not in app.config:
            app.config['routes'] = []

        route = {'fqdn': args.fqdn, 'port': 80}
        if args.https:
            route['https'] = True
            route['port'] = 443
        if args.port:
            route['port'] = args.port

        for r in app.config['routes']:
            if r == route:
                log.die('A route with those options already exists!')

        app.config['routes'].append(route)

        log.action('Route created')
    elif args.do == 'del':
        log.doing('Removing route...')
        if 'routes' not in app.config:
            log.die('No routes created!')

        if args.index < 1 or args.index > len(app.config['routes']):
            log.die('No route with that index!')

        del app.config['routes'][args.index - 1]

        log.action('Route removed')
