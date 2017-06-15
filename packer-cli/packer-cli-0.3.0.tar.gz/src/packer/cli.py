"""
Console script for packer
"""

import enum
import json

import click

class Action(enum.Enum):
    """
    Data transformation action
    """

    MINIMIZE = 'minimize'
    PRETTY = 'pretty'
    VALIDATE = 'validate'

@click.group()
def packer_cli():
    """
    Packer is a simple command line utility for converting data into different
    formats or just changing the formatting of data without changing it to
    a different language.
    """

@packer_cli.command(name='json')
@click.option(
    '--action', '-a',
    type=click.Choice([a.value for a in Action]),
    default=Action.PRETTY.value,
    help='The action to perform on the data')
@click.option(
    '--source', '-s',
    default='-',
    help='The source file to read data from')
def json_formatter(action: str, source: str):
    """
    Formatting for JSON data
    """

    with click.open_file(source, 'r') as source_stream:
        try:
            json_data = json.load(source_stream) # type: ignore
        except json.JSONDecodeError:
            click.secho('Malformed JSON given', err=True, fg='red')
            raise click.Abort()

    if action == Action.PRETTY.value:
        click.echo(json.dumps(json_data, indent=4))
    elif action == Action.MINIMIZE.value:
        click.echo(json.dumps(json_data))
    elif action == Action.VALIDATE.value:
        click.secho('Data is valid!', fg='green')

if __name__ == '__main__':
    packer_cli()
