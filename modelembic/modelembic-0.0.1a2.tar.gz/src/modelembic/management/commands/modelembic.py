# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import sys

import os
from django.core.management import BaseCommand
from django.core.management import CommandError
from django.core.management import CommandParser

from modelchemy import dbs

from modelembic.management.subcommands import BranchesSubCommand
from modelembic.management.subcommands import CurrentSubCommand
from modelembic.management.subcommands import DowngradeSubCommand
from modelembic.management.subcommands import HeadsSubCommand
from modelembic.management.subcommands import HistorySubCommand
from modelembic.management.subcommands import InitSubCommand
from modelembic.management.subcommands import ListTemplatesSubCommand
from modelembic.management.subcommands import MergeSubCommand
from modelembic.management.subcommands import ShowSubCommand
from modelembic.management.subcommands import StampSubCommand
from modelembic.management.subcommands import UpgradeSubCommand
from modelembic.management.subcommands import RevisionSubCommand

MODELEMBIC_COMMANDS = ('branches', 'current', 'downgrade',
                       'heads', 'history', 'init',
                       'list-templates', 'merge',
                       'revision', 'show', 'stamp',
                       'upgrade')


class Command(BaseCommand):
    def run_from_argv(self, argv):

        self._called_from_command_line = True

        parser = self.create_parser(argv[0], argv[1])

        options, argv_unknowns = parser.parse_known_args(argv[2:])

        if len(argv_unknowns) == 0:

            if options.traceback:
                raise CommandError('Missing database alias or key.')

            self.stderr.write('CommandError: Missing database alias or key.')
            sys.exit(1)

        new_argv = [argv[0], argv[1]]
        new_argv.extend(argv_unknowns)

        db_id_parser = CommandParser(
            self, prog="%s %s" % (
                os.path.basename(new_argv[0]), new_argv[1]),
            description=self.help or None,
        )
        db_id_parser.add_argument('database', nargs=1)

        parsed_db_id, unparsed = db_id_parser.parse_known_args(new_argv[2:])

        database_id = parsed_db_id.database[0]

        if database_id not in dbs.keys:

            if database_id in MODELEMBIC_COMMANDS:
                if options.traceback:
                    raise CommandError(
                        'Command invocation without database id.')

                self.stderr.write(
                    'CommandError: Command invocation without database id.')
                sys.exit(1)

            if options.traceback:
                raise CommandError('Database alias or key not found.')

            self.stderr.write('CommandError: Database alias or key not found.')
            sys.exit(1)

        db_id_parser = CommandParser(
            self, prog="%s %s %s" % (
                os.path.basename(new_argv[0]), new_argv[1],
                database_id),
            description=self.help or None,
        )
        db_id_parser.add_argument('cmd', nargs=1)

        parsed_db_id, unparsed = db_id_parser.parse_known_args(unparsed)

        subcmd = parsed_db_id.cmd[0]

        if subcmd not in MODELEMBIC_COMMANDS:
            if options.traceback:
                raise CommandError('Invalid Command.')

            self.stderr.write('CommandError: Invalid Command.')
            sys.exit(1)

        self.handle_subcommnad(argv[0], argv[1], database_id, options, subcmd,
                               unparsed)

    def handle_subcommnad(self, root, cmd, database, options, subcmd, argvs):
        cmd_type = None

        if subcmd == 'show':
            cmd_type = ShowSubCommand(root, cmd, database,
                                      options, self.stdout, self.stderr,
                                      True)
        elif subcmd == 'branches':
            cmd_type = BranchesSubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)
        elif subcmd == 'current':
            cmd_type = CurrentSubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)
        elif subcmd == 'downgrade':
            cmd_type = DowngradeSubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)
        elif subcmd == 'upgrade':
            cmd_type = UpgradeSubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)
        elif subcmd == 'heads':
            cmd_type = HeadsSubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)
        elif subcmd == 'history':
            cmd_type = HistorySubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)
        elif subcmd == 'init':
            cmd_type = InitSubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)
        elif subcmd == 'list-templates':
            cmd_type = ListTemplatesSubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)
        elif subcmd == 'merge':
            cmd_type = MergeSubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)
        elif subcmd == 'stamp':
            cmd_type = StampSubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)
        elif subcmd == 'revision':
            cmd_type = RevisionSubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)

        if cmd_type is not None:
            cmd_type.run_from_argv(argvs)
        else:
            if options.traceback:
                raise CommandError('Invalid Command.')

            self.stderr.write('CommandError: Invalid Command.')
            sys.exit(1)
