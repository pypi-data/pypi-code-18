# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals,print_function
from alembic.script import ScriptDirectory

from alembic.environment import EnvironmentContext
from modelchemy import dbs
from modelembic.management.subcommands.base import BaseSubCommand
from django.core.management.base import CommandError
from sqlalchemy.engine import url
from alembic import util
from alembic import autogenerate as autogen


class RevisionSubCommand(BaseSubCommand):
    help = 'Create a new revision file.'

    def add_arguments(self, parser):

        parser.add_argument('-m', '--message',
                            nargs='?',
                            help="Message string to use with 'revision'")

        parser.set_defaults(message=None)

        parser.add_argument('--autogenerate',
                            dest='autogenerate',
                            help="Populate revision script with candidate "
                                 "migration operations, based on comparison "
                                 "of database to model.",
                            action='store_true')

        parser.set_defaults(autogenerate=False)

        parser.add_argument('--sql',
                            dest='sql',
                            help="Don't emit SQL to database - dump to "
                                 "standard output/file instead",
                            action='store_true')

        parser.set_defaults(sql=False)

        parser.add_argument('--head',
                            nargs='?',
                            help="Specify head revision or "
                                 "<branchname>@head to base new "
                                 "revision on.")

        parser.set_defaults(head=None)

        parser.add_argument('--splice',
                            dest='splice',
                            help="Allow a non-head revision as "
                                 "the 'head' to splice onto",
                            action='store_true')

        parser.set_defaults(splice=False)

        parser.add_argument('--branch-label',
                            dest="branch_label",
                            nargs='?',
                            help="Specify a branch label to "
                                 "apply to the new revision")

        parser.set_defaults(branch_label=None)

        parser.add_argument('--version-path',
                            dest="version_path",
                            nargs='?',
                            help="Specify specific path from "
                                 "config for version file")

        parser.set_defaults(version_path=None)

        parser.add_argument('--rev-id',
                            dest="rev_id",
                            nargs='?',
                            help="Specify a hardcoded revision "
                                 "id instead of generating one")

        parser.set_defaults(rev_id=None)

        parser.add_argument('--no-metadata',
                            dest='use_metadata',
                            help="Avoid passing the metadata "
                                 "to revision environment.",
                            action='store_false')

        parser.set_defaults(use_metadata=True)

        parser.add_argument('--not-use-environment',
                            dest='use_environment',
                            help="Run revision without environment.",
                            action='store_false')

        parser.set_defaults(use_environment=True)

    @staticmethod
    def obfuscate_url_pw(u):
        u = url.make_url(u)
        if u.password:
            u.password = 'XXXXX'
        return str(u)

    @property
    def subcommand(self):
        return 'revision'

    @staticmethod
    def _if_autogenerate_in_command(sql, script, template_args):
        if sql:
            raise CommandError(
                "Using --sql with --autogenerate does not make any sense")

        def retrieve_migrations(rev, context):
            if set(script.get_revisions(rev)) != set(
                    script.get_revisions("heads")):
                raise CommandError("Target database is not up to date.")

            # assert False, context.opts["target_metadata"]
            # assert False, dir(autogen)
            # autogen._render_migration_diffs()
            autogen._render_migration_diffs(context, template_args)
            # autogen._render_migration_diffs(context, template_args, imports)
            return []

        return retrieve_migrations

    def handle(self, *args, **options):
        use_metadata = options.get("use_metadata")
        environment = options.get("use_environment")
        autogenerate = options.get("autogenerate")
        sql = options.get("sql")
        splice = options.get("splice")
        message = options.get("message")
        head = options.get("head")
        branch_label = options.get("branch_label")
        version_path = options.get("version_path")
        rev_id = options.get("rev_id")

        conf_dict = self.get_migrations_config()
        config = self.instantiate_config(conf_dict)

        setattr(config, 'factory', dbs.get(self._database))
        setattr(config, 'use_target_metadata', use_metadata)

        script = ScriptDirectory.from_config(config)
        template_args = {
            'config': config,
        }
        imports = set()
        if autogenerate:
            environment = True

            retrieve_migrations = \
                RevisionSubCommand._if_autogenerate_in_command(sql,
                                                    script,
                                                    template_args)

        elif environment:
            def retrieve_migrations(rev, context):
                return []

        elif sql:
            raise CommandError(
                "Using --sql with the revision command when "
                "revision_environment is not configured does not make any sense")

        RevisionSubCommand._run_environment(config, environment, retrieve_migrations,
                                 script, sql, template_args)

        script.generate_revision(
            rev_id or util.rev_id(), message, refresh=True,
            head=head, splice=splice, branch_labels=branch_label,
            version_path=version_path, **template_args)

    @staticmethod
    def _run_environment(config, environment, retrieve_migrations, script, sql,
                         template_args):
        if environment:
            with EnvironmentContext(
                    config,
                    script,
                    fn=retrieve_migrations,
                    as_sql=sql,
                    template_args=template_args,
            ):
                script.run_env()