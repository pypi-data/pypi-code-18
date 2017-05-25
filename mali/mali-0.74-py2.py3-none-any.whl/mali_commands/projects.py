# coding=utf-8
import click
import requests

from mali_commands.tables import dict_to_csv
from .commons import add_to_data_if_not_none
from terminaltables import PorcelainTable


@click.group('projects')
def projects_commands():
    pass


@projects_commands.command('list')
@click.pass_context
def list_projects(ctx):
    from .commons import handle_api

    result = handle_api(ctx.obj, requests.get, 'projects')

    format_tables = ctx.obj.output_format == 'tables'

    if result is not None:
        if format_tables:
            fields = ['project_id', 'display_name', 'description', 'token', 'org']
            table_data = list(dict_to_csv(result.get('projects', []), fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            click.echo(result)


@projects_commands.command('create')
@click.option('--displayName', required=True)
@click.option('--description', required=False)
@click.option('--org', required=False)
@click.pass_context
def create_project(ctx, displayname, description, org):
    from .commons import handle_api

    data = {}

    add_to_data_if_not_none(data, displayname, "display_name")
    add_to_data_if_not_none(data, org, "org")
    add_to_data_if_not_none(data, description, "description")

    result = handle_api(ctx.obj, requests.post, 'projects', data)

    format_tables = ctx.obj.output_format == 'tables'

    if result is not None:
        if format_tables:
            fields = ['id', 'token']
            table_data = list(dict_to_csv(result, fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            click.echo(result)


@projects_commands.command('transfer')
@click.option('--projectId', required=True)
@click.option('--transferTo', required=False)
@click.pass_context
def transfer_project(ctx, projectid, transferto):
    from .commons import handle_api

    data = {}

    add_to_data_if_not_none(data, transferto, "transfer_to")

    result = handle_api(
        ctx.obj, requests.post, 'projects/{project_id}/transfer'.format(project_id=projectid), data)

    format_tables = ctx.obj.output_format == 'tables'

    if result is not None:
        if format_tables:
            fields = ['ok']
            table_data = list(dict_to_csv(result, fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            click.echo(result)
