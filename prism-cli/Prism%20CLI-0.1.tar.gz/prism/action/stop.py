#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

from ..deco import header, require_app, log_group
from .. import log

from .. import service


@header('Stopping App')
@require_app
@log_group('Stopping application service...', 'Service stopped')
def run(app, args):
    service.stop(app, args)
