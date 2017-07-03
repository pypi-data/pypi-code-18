import os
import sys
from os import path

import click

from dashbase.cli import parameters
from dashbase.cli.constants import (
    DASHBASE_DEFAULT_HOME, DASHBASE_DEFAULT_CLI_CONFIG, DASHBASE_DEFAULT_APP_CONFIG,
    DEFAULT_MIRROR)
from dashbase.utils import configParser

CONTEXT_SETTINGS = dict(auto_envvar_prefix='COMPLEX')


class Context(click.Context):
    def __init__(self, *args, **kwargs):

        self.config = configParser.ConfigParser(
            src=path.join(DASHBASE_DEFAULT_HOME, DASHBASE_DEFAULT_CLI_CONFIG),
            default={
                "verbose": False,
                "debug": False
            })
        self.app_config = None

    @staticmethod
    def log(msg, *args):
        """Logs a message to stderr."""
        if args:
            msg.format(args)
        click.secho(msg, file=sys.stderr, fg='yellow')

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.config.get("verbose"):
            self.log(msg, *args)

    def dlog(self, msg, *args):
        """Logs a message to stderr only if debug is enabled."""
        if self.config.get("debug"):
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = path.abspath(path.join(path.dirname(__file__), "cmd"))


def modify_usage_error():
    """
    Function to modify the default click error handling.
    Used here to tell the user about how to find additional help.
    With thanks to this Stack Overflow answer: http://stackoverflow.com/a/43922088/713980
    :return: None
    """

    def show(self, file=None):
        if file is None:
            file = click._compat.get_text_stderr()
        color = None
        if self.ctx is not None:
            color = self.ctx.color
            click.secho(self.ctx.get_help() + '\n', file=file, color=color)
        click.secho('Error: %s' % self.format_message(), fg='red', file=file, color=color)

    click.exceptions.UsageError.show = show

modify_usage_error()


class ComplexCLI(click.Group):
    def list_commands(self, ctx):
        rv = []
        if not os.path.isdir(cmd_folder):
            return rv
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            func_name = "cmd_{}".format(name)
            import_path = "dashbase.cli.cmd.{}".format(name)
            mod = __import__(import_path, None, None, [func_name])
        except ImportError:
            return
        try:
            mod = getattr(mod, func_name)
        except AttributeError:
            return
        return mod


@click.command(cls=ComplexCLI, context_settings=CONTEXT_SETTINGS)
@click.option('--config',
              type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help='Custom dashbase-cli configuration.')
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@click.option('--mirror', type=parameters.MIRROR, required=False,
              help='Alternative mirror for download.', envvar="DASHBASE_MIRROR")
@click.option('--version', type=parameters.VERSION, required=False,
              help='Specify a version to install.')
@click.option('--debug', is_flag=True,
              help='Enables debug mode.')
@pass_context
def root(ctx, config, verbose, mirror, version, debug):
    """Dashbase CLI"""
    default_dashbase(ctx)
    if config:
        ctx.config = configParser.ConfigParser(src=config)
    if not mirror:
        mirror = DEFAULT_MIRROR
    ctx.config.set('mirror', mirror)
    if version:
        ctx.config.set('version', version)
    ctx.config.set('verbose', verbose)
    ctx.config.set('debug', debug)


def default_dashbase(ctx):
    if not os.path.exists(DASHBASE_DEFAULT_HOME):
        os.makedirs(DASHBASE_DEFAULT_HOME)

    config_file = os.path.join(DASHBASE_DEFAULT_HOME,
                               DASHBASE_DEFAULT_CLI_CONFIG)
    if not os.path.exists(config_file):
        default_config = open(config_file, "w+")
        default_config.write("home: {}\n".format(DASHBASE_DEFAULT_HOME))
        default_config.write("index: /data/index/\n")
        default_config.close()
    ctx.config = configParser.ConfigParser(src=config_file)

    app_config_file = os.path.join(DASHBASE_DEFAULT_HOME,
                                   DASHBASE_DEFAULT_APP_CONFIG)
    if os.path.exists(app_config_file):
        ctx.app_config = configParser.ClusterConfigParser(src=app_config_file)
