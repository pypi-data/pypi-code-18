import click

from dashbase.cli.cli import pass_context
from dashbase.cli.constants import DashbaseService
from dashbase.cli.utils import find_zk_path, find_extensions_path
from dashbase.services import JarService
from dashbase.utils.formatter import Table


@click.command('config', short_help='Initializes and prints Dashbase configs.')
@pass_context
def cmd_config(ctx):
    home = ctx.config.get("home")
    table = Table()
    table.set_cols_dtype(["k", "v"])
    table.add_row(["Home:", home])
    table.add_row(["Index:", ctx.config.get("index")])
    table.add_row(["Table Jar:", JarService.find_jar_path(DashbaseService.TABLE, home)])
    table.add_row(["API Jar:", JarService.find_jar_path(DashbaseService.API, home)])
    table.add_row(["Web Jar:", JarService.find_jar_path(DashbaseService.WEB, home)])
    table.add_row(["Auth Jar:", JarService.find_jar_path(DashbaseService.AUTH, home)])
    table.add_row(["Dashbase Extensions:", find_extensions_path(home)])
    table.add_row(["ZooKeeper:", find_zk_path(home)])
    click.secho(table.draw())
