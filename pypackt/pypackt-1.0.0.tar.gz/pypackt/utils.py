# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from getpass import getpass
try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser

from six.moves import input

from crontab import CronTab

from pypackt.settings import BOOKS_SECTION
from pypackt.settings import LOGIN_KEY
from pypackt.settings import LOGIN_SECTION
from pypackt.settings import PASS_KEY
from pypackt.settings import USER_CONF_FILE


def get_config_parser():
    """Returns initialized configuration parser.

    :return: parser
    :rtype: SafeConfigParser
    """
    parser = SafeConfigParser()
    parser.read(USER_CONF_FILE)
    return parser


def set_config_option(section, option, value):
    """Sets section's option to a given value and saves configuration to file.

    :param str section: Name of the section to store option under.
    :param str option: Option's name.
    :param value: Option's value.
    """
    parser = get_config_parser()
    parser.set(section, option, value)
    with open(USER_CONF_FILE, 'w') as f:
        parser.write(f)


def get_config_option(section, option):
    """Returns option's value.

    :param str section: Name of the section where option is stored.
    :param str option: Option's name.
    :return: Option's value
    :rtype: str
    """
    parser = get_config_parser()
    return parser.get(section, option)


def set_user_login_data():
    """Sets user's login and password."""
    print('Set Packtpub login details')
    login = input('{}: '.format(LOGIN_KEY.capitalize()))
    password = getpass(str('{}: ').format(PASS_KEY.capitalize()))
    set_config_option(LOGIN_SECTION, LOGIN_KEY, login)
    set_config_option(LOGIN_SECTION, PASS_KEY, password)


def get_user_login_data():
    """Returns user's login and password.

    :rtype: (str, str)
    """
    return (
        get_config_option(LOGIN_SECTION, LOGIN_KEY),
        get_config_option(LOGIN_SECTION, PASS_KEY)
    )


def check_user_login_data():
    """Checks if user's login details have been set."""
    if any(x == 'None' for x in get_user_login_data()):
        print('Login data for packtpub.com is not set - please set it now:')
        set_user_login_data()


def show_user_login_data():
    """Prints user's login and password."""
    print('Packtpub login details')
    print('{0}: {2}\n{1}: {3}'.format(
        LOGIN_KEY.capitalize(), PASS_KEY.capitalize(), *get_user_login_data())
    )


def add_cronjob():
    """Adds pypackt to user's crontab.

    Added job is: @daily pypackt.
    """
    user_cron = CronTab(user=True)
    cmd = 'pypackt'
    if not list(user_cron.find_command(cmd)):
        job = user_cron.new(command=cmd, comment='Job added by pypackt.')
        job.every().dom()
        user_cron.write()
        print('Job "{}" added successfully.'.format(job))
    else:
        print('Job already in crontab.')


def list_books():
    """Prints all books claimed with pypackt."""
    parser = get_config_parser()
    for date, title in parser.items(BOOKS_SECTION):
        print(date, title)


def show_last():
    """Prints title of the most recent book."""
    print(get_config_option(BOOKS_SECTION, 'last'))
