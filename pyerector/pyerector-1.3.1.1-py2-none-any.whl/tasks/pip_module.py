#!/usr/bin/python
# Copyright @ 2017 Michael P. Reilly. All rights reserved.
"""Tasks plugin for Pip."""

import logging

from ..args import Arguments
from ._base import Task

try:
    # there is interference between the logging with pip and pyerector
    import thisdoesnotexist
    #from pip import main as pip_main
except ImportError:
    from ..helper import Subcommand
    pip_main = None

class Pip(Task):
    arguments = Arguments(
        Arguments.List('modules'),
        Arguments.Keyword('requirements'),
    )
    def run(self):
        pip_args = ['install']
        if self.args.requirements:
            pip_args.extend(['--requirement', self.args.requirements])
        if self.args.modules:
            pip_args.extend(self.args.modules)

        if pip_main is None:
            pip_cmd = ['pip'] + pip_args
            Subcommand(tuple(pip_cmd), wait=True, stdin=Subcommand.PIPE)
        else:
            self.logger.debug('pip %s', pip_args)
            # seems that pip changes the logging level
            old_level = logging.getLogger().level
            pip_main(pip_args)
            logging.getLogger().level = old_level

Pip.register()
