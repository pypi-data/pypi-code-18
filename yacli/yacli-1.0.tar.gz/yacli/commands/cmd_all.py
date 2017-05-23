import click, os, subprocess, re
from yacli.cli import pass_context
from git import Repo

from yacli import generic as yg


@click.command('all', short_help='Git/maven command on all projects')
@click.option('-s', '--skipped', is_flag=True, help='Show project which will be skipped')
@click.option('-g', '--git', multiple=True, help='Execute a git command')
@click.option('-m', '--mvn', multiple=True, help='Execute a maven goal')
@click.option('-f', '--fast', is_flag=True, default=False, help='No deep clean and skip test')
@click.option('-p', '--projects', multiple=True, help='Specify the reactor')
@pass_context
def cli(ctx, skipped, git, mvn, fast, projects):
    """Update all projects"""

    if skipped :
        yg.actito_project(ctx, projects=projects)
        exit(0)

    # Git
    with click.progressbar(yg.actito_project(ctx, projects=projects)) as projectList:
        for project in projectList:
            for cmd in git:
                yg.git_call(project, cmd)

    # Maven
    for cmd in mvn:
        exec_cmd(ctx, projects, cmd, fast)


def exec_cmd(ctx, projects, cmd, fast):
    fast_param = '' if not fast else "-DskipTests=true -Dmaven.test.skip -Pno-deep-clean"

    if projects :
        poms = [x for sublist in [ x.split(",") for x in projects ] for x in sublist]
        for pom in poms :
            yg.mvn_call("{}/{}/pom.xml".format(ctx.home, pom), cmd, fast_param, '-fae')
    else:
        yg.mvn_call("{}/actito-all/pom.xml".format(ctx.home), cmd, fast_param, '-fae')



