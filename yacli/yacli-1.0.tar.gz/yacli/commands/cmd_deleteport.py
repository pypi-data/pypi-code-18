import click, os, subprocess
from yacli.cli import pass_context, __location__
from git import Repo


PATH = os.path.join(__location__, 'scripts')

@click.command('deleteport', short_help='Delete process which use the port.')
@click.argument('port', required=True)
@pass_context
def cli(ctx, port):
    """Delete process which use the port"""

    stdout = click.get_text_stream('stdout')

    cmd="bash {}/delete_port.sh {}".format(PATH,port)
    subprocess.call(cmd.split(), stdout=stdout, stderr=stdout)
