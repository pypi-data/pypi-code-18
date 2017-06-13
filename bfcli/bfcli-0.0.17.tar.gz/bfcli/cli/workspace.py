import sys

import click
import terminaltables

from bfcli import config
from bfcli.lib.api import API, me
from bfcli.lib.cli_common import sort_flag
from bfcli.lib.environments import WS_TYPES

@click.group()
def workspace():
  config.ensure_config_is_valid()


@workspace.command()
@click.argument('id')
def rm(id):
  """Deletes the workspace with the given ID."""
  ws = API.Workspace.get(id)
  ws.delete()
  click.echo('Deleted workspace:' + str(ws))


@workspace.command()
@click.argument('id')
def save(id):
  """Deletes the workspace with the given ID."""
  ws = API.Workspace.get(id)
  ws.save()
  click.echo('Saved workspace:' + str(ws))


@workspace.command()
@click.argument('id')
def info(id):
  """Prints the workspace with the given ID"""
  ws = API.Workspace.get(id)
  click.echo(str(ws))


@workspace.command()
@sort_flag
def list(sort_created):
  """List all of the currently running workspaces"""
  spaces = API.Workspace.get_all()
  if sort_created:
    spaces = sorted(spaces,
                    key=lambda ws: ws.data.get('start_date'),
                    reverse=(sort_created == 'des'))

  output = ''

  if not spaces:
    click.echo('\nNo active workspaces\n')
    return

  for ws in spaces:
    output += str(ws)

  click.echo(output)


@workspace.command()
@click.argument('platform_type', type=click.Choice(WS_TYPES))
@click.option('--name', '-N', help='The name for your workspace. If not given, it will be auto generated')
@click.option('--gpus', '-g', type=int, help='A comma-separated list of GPU IDs to attach to the workspace')
#@click.option('--node', '-n', 'node_id', type=int, help='(Required) The ID of the Node to run this workspace on')
#@click.option('--gpu-ids', '-g', default='', help='A comma-separated list of GPU IDs to attach to the workspace')
def create(platform_type, name, gpus):
  """Runs a workspace on a node"""

  meta = API.Workspace.image_metadata(platform_type)
  options = {}
  for param in meta.get('parameters', []):
    if 'user_input' in param:
      field_prompt = param.get('display', param['key'])
      val = click.prompt('Enter {}'.format(field_prompt))
      options[param['key']] = val


  ws = API.Workspace.create(platform_type,
                            me().data['user']['defaultGroup'],
                            name=name,
                            gpus=gpus,
                            options=options)

  click.echo(str(ws))

