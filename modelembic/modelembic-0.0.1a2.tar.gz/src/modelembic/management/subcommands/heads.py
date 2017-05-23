# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals,print_function
from alembic.script import ScriptDirectory

from modelchemy import dbs
from modelembic.management.subcommands.base import BaseSubCommand


class HeadsSubCommand(BaseSubCommand):
    help = 'Show current available heads in the script directory'

    def add_arguments(self, parser):

        parser.add_argument('--no-metadata',
                            dest='use_metadata',
                            help="Avoid passing the metadata to "
                                 "revision environment.",
                            action='store_false')

        parser.set_defaults(use_metadata=True)

        parser.add_argument('--verbose',
                            dest='verbose',
                            action='store_true')

        parser.set_defaults(verbose=False)

        parser.add_argument('--resolve-dependencies',
                            dest='resolve_dependencies',
                            action='store_true')

        parser.set_defaults(verbose=False)

    @property
    def subcommand(self):
        return 'heads'

    def handle(self, *args, **options):
        use_metadata = options.get("use_metadata")
        verbose = options.get("verbose")
        resolve_dependencies = options.get("resolve_dependencies")
        conf_dict = self.get_migrations_config()
        config = self.instantiate_config(conf_dict)

        setattr(config, 'factory', dbs.get(self._database))
        setattr(config, 'use_target_metadata', use_metadata)

        script = ScriptDirectory.from_config(config)
        if resolve_dependencies:
            heads = script.get_revisions("heads")
        else:
            heads = script.get_revisions(script.get_heads())
        for rev in heads:
            self.stdout.write(
                rev.cmd_format(
                    verbose, include_branches=True, tree_indicators=False))