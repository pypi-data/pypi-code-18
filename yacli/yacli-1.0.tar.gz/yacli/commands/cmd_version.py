import click, os, subprocess
from yacli.cli import pass_context
from git import Repo


@click.command('version', short_help='Update versions for a project')
@click.argument('project', required=True)
@click.option('-s', '--snapshot', help='Set new snapshot versions')
@click.option('-r', '--revert', 'action', flag_value='revert', help='Revert change not commited')
@click.option('-c', '--commit', 'action', flag_value='commit', help='Commit change')
@pass_context
def cli(ctx, project, snapshot, action):
    """Update versions for a project"""

    pom_path = "{}/{}/pom.xml".format(ctx.home, project)
    if not os.path.isfile(pom_path):
        ctx.log('Unable to find file {}'.format(pom_path))
        return

    if (snapshot) :
        cmd="versions:set -DnewVersion={}-SNAPSHOT".format(snapshot)
        execute_mvn_cmd(ctx, project, cmd)

    if action is not None:
        cmd="versions:{}".format(action)
        execute_mvn_cmd(ctx, project, cmd)


def execute_mvn_cmd(ctx, project, mvn_cmd):
    mvn_prefix="mvn -f {}/{}/pom.xml ".format(ctx.home, project)
    cmd= mvn_prefix + mvn_cmd

    subprocess.call(cmd.split())
