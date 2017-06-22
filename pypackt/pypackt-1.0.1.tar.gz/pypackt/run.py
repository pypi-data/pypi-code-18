# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import argparse

from pypackt import utils
from pypackt.settings import PROJECT_DESC
from pypackt.spider import run_spider


def main():
    parser = argparse.ArgumentParser(description=PROJECT_DESC)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-c', '--configure',
        help='Configure login and password to www.packtpub.com.',
        action='store_true'
    )
    group.add_argument(
        '-l', '--last',
        help='Show last claimed book.',
        action='store_true'
    )
    group.add_argument(
        '-ls', '--list',
        help='List all books claimed with pypackt.',
        action='store_true'
    )
    group.add_argument(
        '-cr', '--cron',
        help="Add job to user's crontab to claim free ebooks daily.",
        action='store_true'
    )
    group.add_argument(
        '-s', '--show',
        help='Show login settings.',
        action='store_true'
    )

    parsed_args = parser.parse_args()
    choices = {
        parsed_args.configure: utils.set_user_login_data,
        parsed_args.last: utils.show_last,
        parsed_args.list: utils.list_books,
        parsed_args.cron: utils.add_cronjob,
        parsed_args.show: utils.show_user_login_data,
    }
    utils.check_user_login_data()
    choices.get(True, run_spider)()
