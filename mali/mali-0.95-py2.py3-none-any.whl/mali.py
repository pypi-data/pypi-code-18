# coding=utf-8
import click
from mali_commands import auth_commands, projects_commands, orgs_commands
from mali_commands.config import Config


class Expando(object):
    pass

@click.group()
@click.option('--apiHost', default='https://missinglinkai.appspot.com', required=False)
@click.option('--host', default='https://missinglink.ai', required=False)
@click.option('--clientId', default='nbkyPAMoxj5tNzpP07vyrrsVZnhKYhMj', required=False)
@click.option('--auth0', default='missinglink', required=False)
@click.option('--outputFormat', '-o', type=click.Choice(['tables', 'json']), default='tables', required=False)
@click.pass_context
def cli(ctx, apihost, host, clientid, auth0, outputformat):
    ctx.obj = Expando()

    ctx.obj.api_host = apihost
    ctx.obj.host = host
    ctx.obj.client_id = clientid
    ctx.obj.auth0 = auth0
    ctx.obj.output_format = outputformat

    config = Config()
    ctx.obj.refresh_token = config.refresh_token
    ctx.obj.id_token = config.id_token

cli.add_command(auth_commands)
cli.add_command(projects_commands)
cli.add_command(orgs_commands)

if __name__ == "__main__":
    cli()
