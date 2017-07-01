#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

from ..deco import header, require_app, log_group

from .. import service


@header('Starting App')
@require_app
@log_group('Starting application service...', 'Service started')
def run(app, args):
    # Create the service files
    service.create(app, args)

    # Enable the service
    service.enable(app, args)

    # Start the service
    service.start(app, args)
