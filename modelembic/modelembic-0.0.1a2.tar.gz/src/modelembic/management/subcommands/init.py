# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals,print_function
import os
from alembic.script import ScriptDirectory
from django.core.management.base import CommandError
from modelembic.management.subcommands.base import BaseSubCommand


class InitSubCommand(BaseSubCommand):
    help = 'Initialize a new scripts directory.'

    def add_arguments(self, parser):

        parser.add_argument('-t', '--template',
                            help="Template to use in the creation of the directory.",
                            default="generic",
                            nargs="?")

    @property
    def subcommand(self):
        return 'init'

    @staticmethod
    def _validate_template_dir(template, templates_directory):
        template_dir = os.path.join(templates_directory, template)
        if not os.access(template_dir, os.F_OK):
            raise CommandError("No such template %r" % template)
        return template_dir

    @staticmethod
    def _get_script_location_directory(migrations_conf_dict):
        directory = migrations_conf_dict.get("script_location", None)
        if directory is None:
            raise CommandError("Invalid Migration Scripts Location")
        if os.access(directory, os.F_OK):
            raise CommandError("Directory %s already exists" % directory)
        return directory

    def get_default_templates_location(self):
        return os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(
                            __file__)))),
            "templates")

    def handle(self, *args, **options):
        template = options.get("template")

        migrations_conf_dict = self.get_migrations_config()

        directory = \
            self._get_script_location_directory(migrations_conf_dict)

        templates_directory = \
            migrations_conf_dict.get("templates_directory",
                                     self.get_default_templates_location())

        template_dir = self._validate_template_dir(template,
                                                   templates_directory)

        self.stdout.write("Creating directory %s" % os.path.abspath(directory))
        os.makedirs(directory)

        versions = os.path.join(directory, 'versions')
        self.stdout.write("Creating directory %s" % os.path.abspath(versions))
        os.makedirs(versions)

        script = ScriptDirectory(directory)
        for file_ in os.listdir(template_dir):
            file_path = os.path.join(template_dir, file_)
            if os.path.isfile(file_path):
                output_file = os.path.join(directory, file_)
                script._copy_file(
                    file_path,
                    output_file
                )