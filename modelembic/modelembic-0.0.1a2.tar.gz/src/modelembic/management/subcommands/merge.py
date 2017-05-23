# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from alembic.script import ScriptDirectory

from modelchemy import dbs
from modelembic.management.subcommands.base import BaseSubCommand
from sqlalchemy.engine import url
from alembic import util


class MergeSubCommand(BaseSubCommand):
    help = 'Merge two revisions together.  Creates a new migration file.'

    def add_arguments(self, parser):
        parser.add_argument('revisions',
                            help="one or more revisions, or "
                                 "'heads' for all heads",
                            nargs="+")

        parser.add_argument('-m', '--message',
                            nargs='?',
                            help="Message string to use with 'revision'")
        parser.set_defaults(message=None)

        parser.add_argument('--branch-label',
                            dest="branch_label",
                            nargs='?',
                            help="Specify a branch label to apply to "
                                 "the new revision")
        parser.set_defaults(branch_label=None)

        parser.add_argument('--rev-id',
                            dest="rev_id",
                            nargs='?',
                            help="Specify a hardcoded revision id "
                                 "instead of generating one")

        parser.set_defaults(rev_id=None)

        parser.add_argument('--no-metadata',
                            dest='use_metadata',
                            help="Avoid passing the metadata to "
                                 "revision environment.",
                            action='store_false')
        parser.set_defaults(use_metadata=True)

    @property
    def subcommand(self):
        return 'merge'

    @staticmethod
    def obfuscate_url_pw(u):
        u = url.make_url(u)
        if u.password:
            u.password = 'XXXXX'
        return str(u)

    def handle(self, *args, **options):
        use_metadata = options.get("use_metadata")
        revisions = options.get("revisions")
        message = options.get("message")
        branch_label = options.get("branch_label")
        rev_id = options.get("rev_id")

        conf_dict = self.get_migrations_config()
        config = self.instantiate_config(conf_dict)

        setattr(config, 'factory', dbs.get(self._database))
        setattr(config, 'use_target_metadata', use_metadata)

        script = ScriptDirectory.from_config(config)
        template_args = {
            'config': config
        }
        return script.generate_revision(
            rev_id or util.rev_id(), message, refresh=True,
            head=revisions, branch_labels=branch_label,
            **template_args)
