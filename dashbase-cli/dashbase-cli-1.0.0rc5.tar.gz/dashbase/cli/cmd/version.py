import click

from dashbase.cli.cli import pass_context, root
from dashbase.cli.constants import DashbaseService, list_services, DASHBASE_CLI_VERSION
from dashbase.services import JarService
from dashbase.utils.formatter import Table

LOGO = """
  ____    _    ____  _   _ ____    _    ____  _____
 |  _ \  / \  / ___|| | | | __ )  / \  / ___|| ____|
 | | | |/ _ \ \___ \| |_| |  _ \ / _ \ \___ \|  _|
 | |_| / ___ \ ___) |  _  | |_) / ___ \ ___) | |___
 |____/_/   \_\____/|_| |_|____/_/   \_\____/|_____|
"""


@root.group(invoke_without_command=True)
@click.argument('type', nargs=1, type=click.Choice(list_services()), required=False)
@pass_context
def cmd_version(ctx, type):
    """Get and set Dashbase version."""
    if click.get_current_context().invoked_subcommand is None:
        home = ctx.config.get("home")
        if not type:
            click.secho(LOGO, fg='cyan')
            table = Table()
            table.set_cols_dtype(["k", "v"])
            table.add_row(["CLI Version:", "{}".format(DASHBASE_CLI_VERSION)])
            table.add_row(["------------------", "------------"])
            table.add_row(["Table Version:", JarService.get_jar_version(DashbaseService.TABLE, home)])
            table.add_row(["API Version:", JarService.get_jar_version(DashbaseService.API, home)])
            table.add_row(["Web Version:", JarService.get_jar_version(DashbaseService.WEB, home)])
            table.add_row(["Auth Version:", JarService.get_jar_version(DashbaseService.AUTH, home)])
            click.secho(table.draw())
            return

        versions, current = JarService.get_jar_versions(home_path=home, type=type, exception=True)
        click.secho("Dashbase {} Version:".format(type))
        for version in versions:
            if version == current:
                click.secho(' *  ' + version + ' (using)', fg="green")
                continue
            click.secho('    ' + version)
    ctx.type = type


@cmd_version.command("set", help="")
@click.argument('version', nargs=1, type=click.STRING)
@click.pass_context
@pass_context
def cmd_version_set(ctx, version):
    home = ctx.config.get("home")
    type = ctx.type
    versions, _ = JarService.get_jar_versions(home_path=home, type=type, exception=True)
    if version not in versions:
        click.secho("Could not find dashbase-{} version: {} in local repo.".format(type, version), fg='yellow')
        click.secho("Maybe you need to `dashbase install service {} "
                    "--version {}` first.".format(type, version), fg='yellow')
        return

    JarService.set_default_jar(home, type, version)
    click.secho("Successfully set dashbase-{} version to {}.".format(type, version))
