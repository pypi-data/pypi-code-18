import click, os, subprocess
from yacli.cli import pass_context, __location__
from subprocess import check_output


PATH = os.path.join(__location__, 'scripts')

@click.command('rcproject', short_help='Find project in RC')
@click.argument('projects_already', type=click.Path(exists=True,
    file_okay=True, resolve_path=True), required=True)
@click.option('--release', required=False)
@pass_context
def cli(ctx, release, projects_already):
    """Find project in RC"""

    stdout = click.get_text_stream('stdout')
    stderr = click.get_text_stream('stderr')

    cmd="bash {}/project_in_rc.sh -d {} -f {}".format(PATH, ctx.home, projects_already)

    if release :
        cmd="{} -r {}".format(cmd, release)

    subprocess.call(cmd.split(), stdout=stdout, stderr=stderr)
