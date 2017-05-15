import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


ENV_MAP = {
    'password': 'DJANGO_ADMIN_PASSWORD',
    'username': 'DJANGO_ADMIN_USERNAME',
}


# Environment variable names
ENV_PASSWORD = 'DJANGO_ADMIN_PASSWORD'
ENV_USERNAME = 'DJANGO_ADMIN_USERNAME'


class Command(BaseCommand):
    """
    Command to create/manage admin users.
    """
    help = 'Create an admin user'

    @staticmethod
    def get_option(option_name, **options):
        """
        Get an option from multiple sources.

        If the option has been specified as a command line flag, then
        that value is used. Otherwise we try to find a corresponding
        environment variable. If none of that is found, ``None`` is
        returned.

        Note:
            ``option_name`` must be a key in ``ENV_MAP`` for the
            environment variable lookup to be attempted.

        Args:
            option_name:
                The name of the option to look up. This name is also
                used to find the appropriate environment variable in
                ``ENV_MAP``.
            options:
                Keyword arguments given by the command's argument
                parser.

        Returns:
            The given option's value if one was given, and ``None``
            otherwise.
        """
        # Try to return command line option if given
        opt = options.get(option_name)
        if opt:
            return opt

        # Fall back to environment variable lookup
        return os.environ.get(ENV_MAP.get(option_name))

    def add_arguments(self, parser):
        """
        Add available options to the parser.
        """
        parser.add_argument(
            '-u',
            '--username',
            action='store',
            help='The username to create the admin with',
            type=str)
        parser.add_argument(
            '-p',
            '--password',
            action='store',
            help=('The password to give the admin. Only has an effect when '
                  '--username is specified.'),
            type=str)

    def handle(self, *args, **options):
        """
        Create an admin user based on the given options.
        """
        username = self.get_option('username', **options)
        password = self.get_option('password', **options)

        if not username:
            raise CommandError('--username and --password are required.')

        if not password:
            raise CommandError('--password is required when a username is '
                               'given.')

        user, _ = get_user_model().objects.get_or_create(username=username)

        # Set user info
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True

        user.save()
