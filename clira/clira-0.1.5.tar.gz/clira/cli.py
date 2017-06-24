import click

from .commands.history import history
from .commands.time_report import time_report
from . import utils


@click.group()
@click.pass_context
def cli(context):
    jira = utils.create_jira()

    context.obj = {
        'jira': jira
    }


cli.add_command(history)
cli.add_command(time_report)


if __name__ == "__main__":
    cli()
