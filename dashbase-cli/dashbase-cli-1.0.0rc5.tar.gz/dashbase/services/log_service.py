# -*- coding:utf-8 -*-
import time

import click

from dashbase.cli.constants import DASHBASE_DEFAULT_HOME


class LogService(object):
    """
    Dashbase Log Service
    """
    LOG_FILE = DASHBASE_DEFAULT_HOME + 'debug.log'

    @classmethod
    def _write_file(cls, data):
        file = open(cls.LOG_FILE, 'a+')
        file.write(data)
        file.close()

    @classmethod
    def _time(cls):
        return '[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    @classmethod
    def log(cls, text, show=True, fg='yellow', with_time=True, nl=True):
        if show:
            click.secho(text, fg=fg, nl=nl)
        if with_time:
            text = cls._time() + text
        if nl:
            text += '\n'
        cls._write_file(text)
