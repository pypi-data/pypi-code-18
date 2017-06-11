# coding=utf-8
import click
from mali_commands.config import Config


@click.group('auth')
def auth_commands():
    pass


@auth_commands.command('init')
@click.pass_context
@click.option('--webserver/--disable-webserver', default=True, required=False)
def init_auth(ctx, webserver):
    from .commons import pixy_flow

    ctx.obj.local_web_server = webserver

    access_token, refresh_token, id_token = pixy_flow(ctx.obj)

    config = Config(ctx.obj.config_prefix)

    config.update_and_save({
        'token': {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'id_token': id_token,
        }
    })
