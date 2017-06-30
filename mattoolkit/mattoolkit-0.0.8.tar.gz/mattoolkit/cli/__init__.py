import click

from ..api import api as api_session

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('--server', default=api_session.API_ROOT)
@click.pass_context
def cli(ctx, debug, server):
    ctx.obj['DEBUG'] = debug
    print('Setting API server: ', server)
    api_session.API_ROOT = server


from .import auth
from . import template
from . import job
from . import api
