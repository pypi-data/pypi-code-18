import click

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj['DEBUG'] = debug


from .import auth
from . import template
from . import job
from . import api
