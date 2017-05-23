# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from alembic.environment import EnvironmentContext
from alembic.script import ScriptDirectory

from modelchemy import dbs
from modelembic.management.subcommands.base import BaseSubCommand


class ShowSubCommand(BaseSubCommand):
    help = 'Show the revision(s) denoted by the given symbol'

    def add_arguments(self, parser):

        parser.add_argument('-r',
                            '--revision',
                            help="Name of the revision to show.",
                            nargs="?",
                            type=str)

        parser.add_argument('--no-metadata', dest='use_metadata',
                            help="Avoid passing the metadata "
                                 "to revision environment.",
                            action='store_false')

        parser.set_defaults(use_metadata=True)
        parser.set_defaults(revision="current")

    @property
    def subcommand(self):
        return 'show'

    def handle(self, *args, **options):
        rev = options.get("revision")
        use_metadata = options.get("use_metadata")
        conf_dict = self.get_migrations_config()
        config = self.instantiate_config(conf_dict)

        setattr(config, 'factory', dbs.get(self._database))
        setattr(config, 'use_target_metadata', use_metadata)

        script = ScriptDirectory.from_config(config)

        if rev == "current":
            def show_current(rev, context):
                for sc in script.get_revisions(rev):
                    self.stdout.write(sc.log_entry)
                return []

            with EnvironmentContext(
                    config,
                    script,
                    fn=show_current
            ):
                script.run_env()

        else:
            for sc in script.get_revisions(rev):
                self.stdout.write(sc.log_entry)


