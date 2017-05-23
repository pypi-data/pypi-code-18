# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from alembic.script import ScriptDirectory

from modelchemy import dbs
from modelembic.management.subcommands.base import BaseSubCommand


class BranchesSubCommand(BaseSubCommand):
    help = 'Show current branch points'

    def add_arguments(self, parser):

        parser.add_argument('--no-metadata',
                            dest='use_metadata',
                            help="Avoid passing the metadata "
                                 "to revision environment.",
                            action='store_false')

        parser.set_defaults(use_metadata=True)

        parser.add_argument('--verbose',
                            dest='verbose',
                            action='store_true')

        parser.set_defaults(verbose=False)

    @property
    def subcommand(self):
        return 'branches'

    def handle(self, *args, **options):
        use_metadata = options.get("use_metadata")
        conf_dict = self.get_migrations_config()
        config = self.instantiate_config(conf_dict)
        verbose = options.get("verbose")

        setattr(config, 'factory', dbs.get(self._database))
        setattr(config, 'use_target_metadata', use_metadata)

        script = ScriptDirectory.from_config(config)
        for sc in script.walk_revisions():
            if sc.is_branch_point:
                self.stdout.write(
                    "%s\n%s\n",
                    sc.cmd_format(verbose,
                                  include_branches=True),
                    "\n".join(
                        "%s -> %s" % (
                            " " * len(str(sc.revision)),
                            rev_obj.cmd_format(
                                False,
                                include_branches=True,
                                include_doc=verbose)
                        ) for rev_obj in
                        (script.get_revision(rev) for rev in sc.nextrev)
                    )
                )


