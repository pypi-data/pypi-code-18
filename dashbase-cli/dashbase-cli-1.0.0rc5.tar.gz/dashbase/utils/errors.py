# -*- coding:utf-8 -*-
import click


class NotFound(click.ClickException):
    pass


class NetworkError(Exception):
    pass


class CliRuntimeError(click.ClickException):
    """An exception that Click can handle and show to the user."""

    #: The exit code for this exception
    exit_code = 1

    def __init__(self, message, command=None):
        if click._compat.PY2:
            if message is not None:
                message = message.encode('utf-8')
        Exception.__init__(self, message)
        self.message = message
        self.command = command

    def format_message(self):
        return self.message

    def show(self, file=None):
        from dashbase.services import LogService

        if file is None:
            file = click._compat.get_text_stderr()
        if self.command is not None:
            LogService.log('Command: {}'.format(self.command), show=False)
        click.secho('Error: %s' % self.format_message(), fg='red', file=file)
        LogService.log('Error: %s' % self.format_message(), show=False)
        click.secho('Log is written to {}.'.format(LogService.LOG_FILE), fg='red', file=file)


def handle_network_error(url, status_code):
    if status_code % 100 / 2:
        click.secho('The url is: ', fg='yellow')
        click.secho(url, fg='blue', underline=True)
        click.secho('The returned status code is {}.'.format(status_code), fg='yellow')
        if status_code == 403:
            click.secho('Please check if you have the necessary permissions.', fg='yellow')
        elif status_code == 404:
            click.secho('Please check if the url is correct.', fg='yellow')
        else:
            raise NetworkError("Fetch file error, status code: {}.".format(status_code))
        click.secho('You may need to contact your administrator or support for more information.', fg='yellow')
        raise CliRuntimeError('Fetch File Error')
