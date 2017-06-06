# coding=utf-8
import click
import requests
from mali_commands.tables import dict_to_csv
from .commons import add_to_data_if_not_none, print_as_json
from terminaltables import PorcelainTable


@click.group('orgs')
def orgs_commands():
    pass


@orgs_commands.command('list')
@click.pass_context
def list_orgs(ctx):
    from .commons import handle_api

    result = handle_api(ctx.obj, requests.get, 'orgs')

    format_tables = ctx.obj.output_format == 'tables'

    if result is not None:
        if format_tables:
            fields = ['org', 'display_name']
            table_data = list(dict_to_csv(result.get('orgs', []), fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            print_as_json(result)


@orgs_commands.command('create')
@click.option('--org', required=True)
@click.option('--displayName', required=False)
@click.option('--description', required=False)
@click.pass_context
def create_org(ctx, org, displayname, description):
    from .commons import handle_api

    data = {}

    add_to_data_if_not_none(data,  displayname, 'display_name')
    add_to_data_if_not_none(data, description, 'description')
    add_to_data_if_not_none(data, org, 'org')

    result = handle_api(ctx.obj, requests.post, 'orgs', data)

    format_tables = ctx.obj.output_format == 'tables'

    if result is not None:
        if format_tables:
            fields = ['ok']
            table_data = list(dict_to_csv(result, fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            print_as_json(result)


@orgs_commands.command('autoJoinDomain')
@click.option('--org', required=True)
@click.option('--domain', required=True, multiple=True)
@click.pass_context
def auto_join_domain(ctx, org, domain):
    from .commons import handle_api

    data = {}

    add_to_data_if_not_none(data, list(domain), 'domains')

    result = handle_api(ctx.obj, requests.post, 'orgs/{org}/autoJoin'.format(org=org), data)

    format_tables = ctx.obj.output_format == 'tables'

    if result is not None:
        if format_tables:
            fields = ['ok']
            table_data = list(dict_to_csv(result, fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            print_as_json(result)
