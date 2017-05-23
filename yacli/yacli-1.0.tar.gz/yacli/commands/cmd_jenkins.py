import click, os, subprocess
from yacli.cli import pass_context, __location__
from yacli.generic import GroupMap
from subprocess import check_output

short_help= """ add-job-to-view
    Adds jobs to view.
  build
    Builds a job, and optionally waits until its completion.
  chain
    Chain some build and clear the queue between each build.
  clear-queue
    Clears the build queue.
  connect-node
    Reconnect to a node.
  console
    Retrieves console output of a build.
  get-job
    Dumps the job definition XML to stdout.
  help
    Lists all the available commands or a detailed description of single command.
  list-jobs
    Lists all jobs in a specific view or item group.
  mail
    Reads stdin and sends that out as an e-mail."""

ENVS  = { 
    'build' : "http://vmcosbuildci01.server.citobi.be:8080",
    'dev' : "http://devci.server.citobi.be"
}

PATH = os.path.join(__location__, 'jar')

CLI_CMD = "java -jar {}/jenkins-cli.jar -noKeyAuth -s {} {} {} 2>&1"

CUSTOM_CMD_NAME = [ "status", "head" , "chain"]
CUSTOM_CMD_ARG = {
        "status" : 1,
        "head" : 1,
        "chain" : 1
        }
CUSTOM_CMD_USAGE = {
        "status" : "status job",
        "head" : "head job",
        "chain" : "chain job1 [job2 [job3 [...]]]"
        }
CUSTOM_CMD = {
        "status" : "curl --silent {}/job/{}/lastBuild/api/json \
                | grep -o '\"result\":[^,]*'",
        "head" : "curl --silent {}/job/{}/lastBuild/api/json \
                | grep -o '\"lastBuiltRevision\":[^,]*'"
        }


@click.command('jenkins', short_help='Use jenkins cli')
@click.argument('command', required=True, default='short_help')
@click.argument('argument', nargs=-1)
@click.option('--env', default='build', type=click.Choice(['build', 'dev']))
@pass_context
def cli(ctx, env, command, argument):
    if command == "short_help":
        click.echo(short_help)
        return

    if command == "chain":
        for job in argument:
            execute(env, "build", ["-s -v", job])
            execute(env, "clear-queue", [])
    else:
        execute(env, command, argument)


def execute(env, command, argument):
    stdout = click.get_text_stream('stdout')
    stderr = click.get_text_stream('stderr')

    if command not in CUSTOM_CMD_NAME  :
        to_execute = CLI_CMD.format(PATH, ENVS[env], command, ' '.join(argument))
    else:
        assertArgument(command, argument, 1)
        to_execute = CUSTOM_CMD[command].format(ENVS[env], argument[0])

    subprocess.call(to_execute, shell=True, stdout=stdout, stderr=stderr)


def assertArgument(command, argument, expected_size):
    if len(argument) < expected_size:
        click.echo(CUSTOM_CMD_USAGE[command])
        os._exit(1)

