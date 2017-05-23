import click, os, subprocess, re, sys
from yacli.cli import pass_context, ProjectBranch
from yacli.generic import GroupMap, InvertGroupMap
from subprocess import check_output

from yacli import generic as yg

@click.command('gb', short_help='Find branch')
@click.argument('pattern', default='', required=True)
@click.option('--list', is_flag=True, default=False,  help='List')
@click.option('-l', '--local', 'mode', flag_value='', default=True, help='Operate on local branch')
@click.option('-r', '--remote', 'mode', flag_value='--remote', help='Operate on remote branch')
@click.option('--delete', is_flag=True, default=False,  help='Delete branch')
@click.option('--merged', 'merge', flag_value='--merged', help='Only fully merged branch in develop')
@click.option('--no-merged', 'merge', flag_value='--no-merged', help='Only no merged branch in develop')
@click.option('--current', is_flag=True, default=False, help='Only current branch')
@click.option('--group-by', 
        type=click.Choice([ProjectBranch.GROUP_BY_BRANCH, ProjectBranch.GROUP_BY_PROJECT]),
        default=ProjectBranch.GROUP_BY_BRANCH,  help='Output result')
@pass_context
def cli(ctx, pattern, list, mode, delete, group_by, merge, current):
    """Keep the last release branch and delete others"""

    if ('branch' == group_by):
        output = GroupMap(ctx)
    else:
        output = InvertGroupMap(ctx)

    for project in yg.actito_project(ctx, clean_state=False):
        branches = available_branches(project, mode, merge, current)

        for branch in branches.split() : 
            if pattern in branch and "*" != branch :
                ctx.vlog("Process {}".format(branch))
                output.add(branch, project)

                if (delete):
                    if 'remote' in mode :
                        yg.git_check(project, 'push origin --delete {}'.format(remove_origin(branch)))
                    else :
                        yg.git_check(project, 'branch -D {}'.format(branch))

    if (list) :
        click.echo(output.list_key())
    else :
        click.echo(output.__str__())


def available_branches(project, mode, merge, current):
    if current :
        return yg.git_check(project, 'rev-parse --abbrev-ref HEAD')

    if 'develop' in yg.git_check(project, 'branch --list', mode):
        merge_arg = '{} origin/develop'.format(merge) if merge else ''
        return yg.git_check(project, 'branch --list', mode, merge_arg)
    else:
        return ''


def remove_origin(branch):
    p = re.compile("origin/(.*)")
    return p.match(branch).group(1)
