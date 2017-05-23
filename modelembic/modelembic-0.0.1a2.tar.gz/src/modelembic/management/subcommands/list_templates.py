# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import os

from modelembic.management.subcommands.base import BaseSubCommand


class ListTemplatesSubCommand(BaseSubCommand):
    help = """List available templates"""

    @property
    def subcommand(self):
        return 'list-templates'

    def get_default_templates_location(self):
        return os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(
                            __file__)))),
            "templates")

    def handle(self, *args, **options):

        migrations_conf_dict = self.get_migrations_config()

        templates_directory = \
            migrations_conf_dict.get("templates_directory",
                                     self.get_default_templates_location())

        self.stdout.write("Available templates:\n")
        for tempname in os.listdir(templates_directory):
            with open(os.path.join(templates_directory, tempname,
                                   'README')) as readme:
                synopsis = next(readme)
                self.stdout.write("%s - %s" % (tempname, synopsis))

        self.stdout.write(
            "\nTemplates are used via "
            "the 'alembicate_init' command, e.g.:")

        self.stdout.write(
            "\n  ./manage.py modelembic %s init "
            "--template generic" % self._database)