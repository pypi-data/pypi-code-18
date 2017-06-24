import click
import datetime

from clira.utils import get_timedelta


@click.command()
@click.argument('issue')
@click.pass_context
def time_report(context, issue):
    """Show how much time issue spent in every status"""

    jira = context.obj['jira']

    status_changes = get_data_from_jira(jira, issue)
    time_report = prepare_time_report(status_changes)
    print_time_report(time_report)


def get_data_from_jira(jira, issue):
    issue = jira.issue(issue, expand='changelog')
    changelog = issue.changelog

    data = []
    for history in changelog.histories:
        for item in history.items:
            if item.field == 'status':
                data.append(
                    {
                        'timestamp': history.created,
                        'from_status': item.fromString,
                        'to_status': item.toString
                    }
                )

    return data


def prepare_time_report(status_changes):
    time_report = {}
    for change in status_changes:
        from_status = change['from_status']
        to_status = change['to_status']
        timestamp = change['timestamp']

        if from_status in time_report.keys():
            time_report[from_status]['total'] += get_timedelta(
                time_report[from_status]['start_time'],
                timestamp
            )

        if to_status in time_report.keys():
            time_report[to_status]['start_time'] = timestamp
        else:
            time_report[to_status] = {
                'start_time': timestamp,
                'total': datetime.timedelta(0),
            }

    sorted_time_report = sorted(
        time_report.items(),
        key=lambda result_tuple: result_tuple[1]['total']
    )

    return reversed(sorted_time_report)


def print_time_report(time_report):
    for status, result in time_report:
        click.echo('{} {} {}'.format(
            click.style(status, fg='cyan'),
            click.style('->', fg='yellow'),
            result['total'])
        )
