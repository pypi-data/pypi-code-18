# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals,print_function
from alembic.script import ScriptDirectory
from sqlalchemy.engine import url

from alembic.environment import EnvironmentContext
from modelchemy import dbs
from modelembic.management.subcommands.base import BaseSubCommand
from django.core.management.base import CommandError


class DowngradeSubCommand(BaseSubCommand):
    help = 'Show the revision(s) denoted by the given symbol'

    def add_arguments(self, parser):

        parser.add_argument('revision',
                            help="revision identifier",
                            type=str)

        parser.add_argument('--no-metadata',
                            dest='use_metadata',
                            help="Avoid passing the metadata "
                                 "to revision environment.",
                            action='store_false')

        parser.set_defaults(use_metadata=True)

        parser.add_argument('--sql',
                            dest='sql',
                            help="Don't emit SQL to database - dump "
                                 "to standard output/file instead",
                            action='store_true')

        parser.set_defaults(sql=False)

        parser.add_argument('--tag',
                            dest="tag",
                            nargs='?',
                            help="Arbitrary 'tag' name - can be "
                                 "used by custom env.py scripts.")

        parser.set_defaults(rev_id=None)

    @property
    def subcommand(self):
        return 'downgrade'

    def handle(self, *args, **options):
        use_metadata = options.get("use_metadata")
        sql = options.get("sql")
        tag = options.get("tag")
        revision = options.get("revision", None)
        conf_dict = self.get_migrations_config()
        config = self.instantiate_config(conf_dict)

        setattr(config, 'factory', dbs.get(self._database))
        setattr(config, 'use_target_metadata', use_metadata)

        script = ScriptDirectory.from_config(config)
        starting_rev = None
        if ":" in revision:
            if not sql:
                raise CommandError("Range revision not allowed")
            starting_rev, revision = revision.split(':', 2)
        elif sql:
            raise CommandError(
                "downgrade with --sql requires <fromrev>:<torev>")

        def downgrade(rev, context):
            return script._downgrade_revs(revision, rev)

        with EnvironmentContext(
                config,
                script,
                fn=downgrade,
                as_sql=sql,
                starting_rev=starting_rev,
                destination_rev=revision,
                tag=tag
        ):
            script.run_env()