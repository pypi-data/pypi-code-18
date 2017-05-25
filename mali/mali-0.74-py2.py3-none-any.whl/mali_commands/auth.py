# coding=utf-8
import click
from mali_commands.config import Config


@click.group('auth')
def auth_commands():
    pass


@auth_commands.command('init')
@click.pass_context
def init_auth(ctx):
    from .commons import pixy_flow

    access_token, refresh_token, id_token = pixy_flow(ctx.obj)

    config = Config()

    config.update_and_save({
        'token': {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'id_token': id_token,
        }
    })
