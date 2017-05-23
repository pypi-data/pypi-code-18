# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals,print_function
from alembic.script import ScriptDirectory
from sqlalchemy.engine import url

from alembic.environment import EnvironmentContext
from modelchemy import dbs
from modelembic.management.subcommands.base import BaseSubCommand


class CurrentSubCommand(BaseSubCommand):
    help = 'Show the revision(s) denoted by the given symbol'

    def add_arguments(self, parser):

        parser.add_argument('--no-metadata',
                            dest='use_metadata',
                            help="Avoid passing the metadata "
                                 "to revision environment.",
                            action='store_false')

        parser.add_argument('--verbose',
                            dest='verbose',
                            action='store_true')

        parser.set_defaults(use_metadata=True)
        parser.set_defaults(verbose=False)

    @property
    def subcommand(self):
        return 'current'

    @staticmethod
    def obfuscate_url_pw(u):
        u = url.make_url(u)
        if u.password:
            u.password = 'XXXXX'
        return str(u)

    def handle(self, *args, **options):
        use_metadata = options.get("use_metadata")
        conf_dict = self.get_migrations_config()
        config = self.instantiate_config(conf_dict)
        verbose = options.get("verbose")

        setattr(config, 'factory', dbs.get(self._database))
        setattr(config, 'use_target_metadata', use_metadata)

        script = ScriptDirectory.from_config(config)

        def display_version(rev, context):
            if verbose:
                sql_alchemy_engine = getattr(dbs.get(self._database), "engine",
                                             None)
                self.stdout.write(
                    "Current revision(s) for %s:",
                    self.obfuscate_url_pw(sql_alchemy_engine.url)
                )
            for rev in script.get_revisions(rev):
                self.stdout.write(rev.cmd_format(verbose))
            return []

        with EnvironmentContext(
                config,
                script,
                fn=display_version
        ):
            script.run_env()