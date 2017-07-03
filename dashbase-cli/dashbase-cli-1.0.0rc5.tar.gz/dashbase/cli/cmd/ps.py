import click
import psutil

from dashbase.cli.cli import pass_context
from dashbase.cli.constants import DASHBASE_PROCESS_PREFIX
from dashbase.utils.formatter import Table


@click.command('ps', short_help='List running Dashbase services.')
@pass_context
def cmd_ps(ctx):
    count = 0
    table = Table()
    table.set_cols_dtype(["p", "t", "n", "c"])
    table.add_row(["PID", "TYPE", "NAME", "CONFIG"])
    for proc in psutil.process_iter():
        try:
            if proc.name() == "java" and DASHBASE_PROCESS_PREFIX in " ".join(proc.cmdline()):
                cmd = proc.cmdline()
                type = cmd[1].split("-")[2]
                name = "-".join(cmd[1].split("-")[3:])
                config = cmd[2].split("=")[-1]
                count += 1
                table.add_row([proc.pid, type, name, config])

        except psutil.NoSuchProcess:
            pass
    if count:
        click.secho(table.draw())
    else:
        click.secho("No running Dashbase services found.", fg='yellow')
