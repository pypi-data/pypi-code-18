#!/usr/bin/env python

# coding=utf-8
import click
from mali_commands import auth_commands, projects_commands, orgs_commands, runcode_commands
from mali_commands.config import Config


class Expando(object):
    pass


@click.group()
@click.option('--outputFormat', '-o', type=click.Choice(['tables', 'json']), default='tables', required=False)
@click.option('--configPrefix', required=False)
@click.pass_context
def cli(ctx, outputformat, configprefix):
    ctx.obj = Expando()

    from mali_commands.commons import handle_api

    config = Config(configprefix)

    ctx.obj.config_prefix = configprefix
    ctx.obj.handle_api = handle_api

    ctx.obj.api_host = config.api_host
    ctx.obj.host = config.host
    ctx.obj.client_id = config.client_id
    ctx.obj.refresh_token = config.refresh_token

    ctx.obj.auth0 = config.auth0
    ctx.obj.output_format = outputformat

    ctx.obj.refresh_token = config.refresh_token
    ctx.obj.id_token = config.id_token

cli.add_command(auth_commands)
cli.add_command(projects_commands)
cli.add_command(orgs_commands)
cli.add_command(runcode_commands)


if __name__ == "__main__":
    cli()
