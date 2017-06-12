# coding=utf-8
import json

import click
import requests

from mali_commands.tables import dict_to_csv
from .commons import add_to_data_if_not_none, create_validate_length, print_as_json, print_as_bad_json
from terminaltables import PorcelainTable


@click.group('projects')
def projects_commands():
    pass


@projects_commands.command('list')
# deprecated but some clients use it
@click.option('--outputFormat', '-o', type=click.Choice(['tables', 'json']), default='tables', required=False)
@click.pass_context
def list_projects(ctx, outputformat):
    from .commons import handle_api

    result = handle_api(ctx.obj, requests.get, 'projects')

    json_format = ctx.obj.output_format == 'json'
    bad_json_format = outputformat == 'json'
    format_tables = not json_format and not bad_json_format

    if result is not None:
        if format_tables:
            fields = ['project_id', 'display_name', 'description', 'token', 'org']
            table_data = list(dict_to_csv(result.get('projects', []), fields))

            click.echo(PorcelainTable(table_data).table)
        elif bad_json_format:
            print_as_bad_json(result)
        else:
            print_as_json(result)


max_project_display_name = 140
min_project_display_name = 1

max_project_description = 140
min_project_description = 0


@projects_commands.command('create')
@click.option(
    '--displayName', required=True, callback=create_validate_length(min_project_display_name, max_project_display_name))
@click.option(
    '--description', required=False, callback=create_validate_length(min_project_description, max_project_description))
@click.option('--org', required=False)
# deprecated but some clients use it
@click.option('--outputFormat', '-o', type=click.Choice(['tables', 'json']), default='tables', required=False)
@click.pass_context
def create_project(ctx, displayname, description, org, outputformat):
    from .commons import handle_api

    data = {}

    add_to_data_if_not_none(data, displayname, "display_name")
    add_to_data_if_not_none(data, org, "org")
    add_to_data_if_not_none(data, description, "description")

    result = handle_api(ctx.obj, requests.post, 'projects', data)

    json_format = ctx.obj.output_format == 'json'
    bad_json_format = outputformat == 'json'
    format_tables = not json_format and not bad_json_format

    if result is not None:
        if format_tables:
            fields = ['id', 'token']
            table_data = list(dict_to_csv(result, fields))

            click.echo(PorcelainTable(table_data).table)
        elif bad_json_format:
            print_as_bad_json(result)
        else:
            print_as_json(result)


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
            print_as_json(result)
