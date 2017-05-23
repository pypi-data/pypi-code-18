# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals,print_function
from alembic.script import ScriptDirectory

from alembic.environment import EnvironmentContext
from modelchemy import dbs
from django.core.management.base import CommandError
from modelembic.management.subcommands.base import BaseSubCommand


class HistorySubCommand(BaseSubCommand):
    help = 'List changeset scripts in chronological order.'

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

        parser.add_argument('-r',
                            dest='rev_range',
                            nargs='?',
                            help="Specify a revision range; "
                                 "format is [start]:[end]")

        parser.set_defaults(rev_range=None)

    @property
    def subcommand(self):
        return 'history'

    def handle(self, *args, **options):
        verbose = options.get("verbose")
        use_metadata = options.get("use_metadata")
        rev_range = options.get("rev_range")
        conf_dict = self.get_migrations_config()
        config = self.instantiate_config(conf_dict)

        setattr(config, 'factory', dbs.get(self._database))
        setattr(config, 'use_target_metadata', use_metadata)

        script = ScriptDirectory.from_config(config)
        if rev_range is not None:
            if ":" not in rev_range:
                raise CommandError(
                    "History range requires [start]:[end], "
                    "[start]:, or :[end]")
            base, head = rev_range.strip().split(":")
        else:
            base = head = None

        def _display_history(config, script, base, head):
            for sc in script.walk_revisions(
                    base=base or "base",
                    head=head or "heads"):
                self.stdout.write(
                    sc.cmd_format(
                        verbose=verbose, include_branches=True,
                        include_doc=True, include_parents=True))

        def _display_history_w_current(config, script, base=None, head=None):
            def _display_current_history(rev, context):
                if head is None:
                    _display_history(config, script, base, rev)
                elif base is None:
                    _display_history(config, script, rev, head)
                return []

            with EnvironmentContext(
                    config,
                    script,
                    fn=_display_current_history
            ):
                script.run_env()

        if base == "current":
            _display_history_w_current(config, script, head=head)
        elif head == "current":
            _display_history_w_current(config, script, base=base)
        else:
            _display_history(config, script, base, head)