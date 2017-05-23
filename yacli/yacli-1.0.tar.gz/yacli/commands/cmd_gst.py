import click, os, subprocess
from yacli.cli import pass_context, ProjectBranch
from git import Repo
from subprocess import check_output

from yacli import generic as yg


@click.command('gst', short_help='Show repository status')
@click.argument('ref', required=False)
@click.option('--all', is_flag=True, default=True, help='Both uncommited and unpushed')
@click.option('--no-commit', is_flag=True, default=False, help='Uncommited change')
@click.option('--no-push', is_flag=True, required=False, help='Unpushed commit')
@pass_context
def cli(ctx, ref, all, no_commit, no_push):
    """Show uncommited change"""

    output = ProjectBranch(ProjectBranch.GROUP_BY_PROJECT)

    for project in yg.actito_project(ctx, clean_state=False):
        ctx.vlog("Process {}".format(project))

        if (all or no_commit) :
            uncommited = yg.git_check(project, 'status --porcelain')
            if uncommited not in "" :
                for fileChange in uncommited.splitlines() :
                    output.add(fileChange, project)

        if (all or no_push) :
            remote_branches = yg.git_check(project, 'branch --remote')
            branches = yg.git_check(project, 'branch')

            for branch in branches.splitlines() : 
                ctx.vlog("\tBranch {}".format(branch))
                branch = branch.replace("*", "").strip().split()[0]

                if "HEAD" in branch:
                    continue

                outputBranch = ProjectBranch(ProjectBranch.GROUP_BY_BRANCH)

                if not ref:
                    try:
                        tmp = findRefBranch(project, branch).split()[0]
                    except Exception:
                        tmp = 'develop'
                else:
                    tmp = ref

                unpushed=None
                try:
                    unpushed =  yg.git_check(project, 'log',
                            '--no-merges {}..{}'.format(tmp, branch),
                            '--pretty=oneline')
                except Exception:
                    ctx.vlog("\tUnable to process {}".format(branch))

                if unpushed and unpushed not in "" :
                    for log in unpushed.splitlines() :
                        outputBranch.add(branch, log)
                    output.add(outputBranch, project)


    click.echo(output.__str__())



def findRefBranch(project, branch):
    return yg.git_check(project, 
            'rev-parse --abbrev-ref {}@{}'.format(branch, "{upstream}"))
