# -*- coding:utf-8 -*-
import os
import shutil

import click

from dashbase.cli.cli import pass_context, root
from dashbase.cli.constants import (list_services,
                                    ZOOKEEPER,
                                    DASHBASE_EXTENSIONS, DashbaseService)
from dashbase.services import JarService
from dashbase.utils.errors import NotFound


@root.group(chain=True)
@pass_context
def cmd_uninstall(ctx):
    """Uninstall a Dashbase service or ZooKeeper"""
    pass


@cmd_uninstall.command('service', short_help='Uninstall a Dashbase service.')
@click.argument('type', nargs=1, type=click.Choice(list_services(True)))
@click.option('--all', is_flag=True, help='Uninstall all versions of the specified type.')
@pass_context
def cmd_uninstall_service(ctx, type, all):
    """Uninstall a Dashbase service jar"""
    home = ctx.config.get('home', '')
    if type == DashbaseService.MONITOR:
        type = DashbaseService.TABLE

    path = os.path.join(home, 'dashbase-{}'.format(type))
    if not os.path.exists(path):
        click.secho("dashbase-{} is not installed.".format(type), fg='yellow')
        return
    if all:
        shutil.rmtree(path)
        click.secho('Successfully uninstalled dashbase-{}.'.format(type))
        return

    path = os.path.join(path, 'target')

    try:
        installed_versions, current_version = JarService.get_jar_versions(type=type, home_path=home, exception=True)
    except NotFound:
        click.secho("dashbase-{} is not installed.".format(type), fg='yellow')
        return
    version = ctx.config.get('version', current_version)
    if installed_versions is None or version not in installed_versions:
        click.secho('`{}` of dashbase-{} is not installed.'.format(version, type), fg='yellow')
        return
    os.remove(os.path.join(path, 'dashbase-{}-{}.jar'.format(type, version)))
    click.secho("Successfully uninstalled `{}` of dashbase-{}.".format(version, type))


@cmd_uninstall.command(ZOOKEEPER, help="Uninstall ZooKeeper")
@pass_context
def cmd_uninstall_zookeeper(ctx):
    """Uninstall ZooKeeper"""
    home = ctx.config.get('home', '')
    if not os.path.exists(os.path.join(home, ZOOKEEPER)):
        click.secho("ZooKeeper is not installed.", fg='yellow')
        return
    shutil.rmtree(os.path.join(home, ZOOKEEPER))
    click.secho("Successfully uninstalled ZooKeeper.")


@cmd_uninstall.command('extensions', help="Uninstall Dashbase extensions.")
@pass_context
def cmd_uninstall_extensions(ctx):
    """Uninstall Dashbase Extensions"""
    home = ctx.config.get('home', '')

    if not os.path.exists(os.path.join(home, DASHBASE_EXTENSIONS)):
        click.secho("{} is not installed.".format(DASHBASE_EXTENSIONS), fg='yellow')
        return
    shutil.rmtree(os.path.join(home, DASHBASE_EXTENSIONS))
    click.secho("Successfully uninstalled Dashbase extensions.")
