# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals,print_function
from alembic.script import ScriptDirectory

from alembic.environment import EnvironmentContext
from modelchemy import dbs
from modelembic.management.subcommands.base import BaseSubCommand
from django.core.management.base import CommandError


class UpgradeSubCommand(BaseSubCommand):
    help = 'Upgrade to a later version.'

    def add_arguments(self, parser):
        parser.add_argument('revision',
                            help="revision identifier",
                            nargs="?",
                            type=str)

        parser.add_argument('--no-metadata',
                            dest='use_metadata',
                            help="Avoid passing the metadata to "
                                 "revision environment.",
                            action='store_false')

        parser.set_defaults(use_metadata=True)

        parser.add_argument('--sql',
                            dest='sql',
                            help="Don't emit SQL to database - dump to "
                                 "standard output/file instead",
                            action='store_true')

        parser.set_defaults(sql=False)

        parser.add_argument('--tag',
                            dest="tag",
                            nargs=1,
                            help="Arbitrary 'tag' name - can be used by "
                                 "custom env.py scripts.")

        parser.set_defaults(rev_id=None)

    @property
    def subcommand(self):
        return 'upgrade'

    def handle(self, *args, **options):
        revision = options.get("revision", None)
        use_metadata = options.get("use_metadata")
        sql = options.get("sql")
        tag = options.get("tag")
        tag = tag[0] if tag is not None else None

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

        def upgrade(rev, context):
            return script._upgrade_revs(revision, rev)

        with EnvironmentContext(
                config,
                script,
                fn=upgrade,
                as_sql=sql,
                starting_rev=starting_rev,
                destination_rev=revision,
                tag=tag
        ):
            script.run_env()