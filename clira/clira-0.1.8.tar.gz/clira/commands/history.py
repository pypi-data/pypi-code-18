import click

from clira.utils import format_time


@click.command()
@click.argument('issue')
@click.pass_context
def history(context, issue):
    """Show issue history"""

    jira = context.obj['jira']

    issue = jira.issue(issue, expand='changelog')
    changelog = issue.changelog

    for history in changelog.histories:
        for item in history.items:
            message = '{} | {} | '.format(
                click.style(format_time(history.created), fg='blue'),
                click.style(item.field, fg='cyan')
            )
            click.echo(message, nl=False)

            detail = '{} {} {}'.format(
                item.fromString,
                click.style('->', fg='yellow'),
                item.toString
            )
            click.echo(detail)
