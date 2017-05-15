import os
from argparse import ArgumentParser

import sys

from gitlabbuildvariables.common import GitLabConfig
from gitlabbuildvariables.manager import ProjectVariablesManager
from typing import List, NamedTuple

from dockerwithgitlabsecrets.configuration import parse_configuration
from dockerwithgitlabsecrets.wrapper import run_wrapped, ProgramOutputType, get_supported_action_index

CONFIG_PARAMETER = "dwgs-config"
PROJECT_PARAMETER = "dwgs-project"
TTY_PARAMETER = "t"
STDIN_OPEN_PARAMETER = "i"

DEFAULT_CONFIG_FILE = f"{os.path.expanduser('~')}/.dwgs-config.yml"

_NAMESPACE_PROJECT_SEPARATOR = "/"


class CliConfiguration(NamedTuple):
    """
    Configuration given via the CLI.
    """
    docker_args: List[str] = []
    config_location: str = None
    project: str = None
    interactive: bool = False


def is_interactive(docker_arguments: List[str]) -> bool:
    """
    Detects whether Docker is to be ran interactively based on the given arguments.
    
    Note: will incorrectly classify as interactive if the command has a `-t` flag, e.g.
    ["run", "--rm", "ubuntu", "command", "-i", "-it", "-ti"]
    Without creating a parser for all Docker commands, it is not possible to get around this issue. However, running a
    non-interactive command interactively should not cause any issues.
    :param docker_arguments: the arguments given to Docker
    :return: whether Docker is to be ran interactively 
    """
    supported_action_index = get_supported_action_index(docker_arguments)
    if supported_action_index is None:
        return False
    return len({f"-{TTY_PARAMETER}", f"-{TTY_PARAMETER}{STDIN_OPEN_PARAMETER}",
                f"-{STDIN_OPEN_PARAMETER}{TTY_PARAMETER}"} & set(docker_arguments[supported_action_index:])) > 0


def parse_cli_arguments(program_args: List[str]) -> CliConfiguration:
    """
    Parse the CLI arguments.
    :param program_args: the CLI arguments
    :return: the configuration given via the CLI 
    """
    if len(program_args) == 0:
        program_args.append("-h")

    add_help = len(program_args) == 1 and program_args[0] in ["-h", "--h"]

    parser = ArgumentParser(description="Docker With GitLab Secrets", add_help=add_help)
    parser.add_argument(
        f"--{CONFIG_PARAMETER}", type=str,
        help=f"location of the configuration file (will default to {DEFAULT_CONFIG_FILE})")
    parser.add_argument(
        f"--{PROJECT_PARAMETER}", type=str,
        help="GitLab project (if not namespaced in the form \"namespace/project\", the default namespace defined in "
             "the configuration file will be used). If not defined, the default project in the configuration file will "
             "be used")

    parsed_program_args, parsed_docker_args = parser.parse_known_args(program_args)
    parsed_program_args = {key.replace("_", "-"):value for key, value in vars(parsed_program_args).items()}

    return CliConfiguration(
        config_location=parsed_program_args[CONFIG_PARAMETER], project=parsed_program_args[PROJECT_PARAMETER],
        interactive=is_interactive(parsed_docker_args), docker_args=parsed_docker_args)


def run(cli_configuration: CliConfiguration) -> ProgramOutputType:
    """
    Runs the program according to the given run configuration. 
    :param cli_configuration: the run configuration
    :return: the run output
    """
    configuration = parse_configuration(cli_configuration.config_location if
                                        cli_configuration.config_location is not None else DEFAULT_CONFIG_FILE)

    project = cli_configuration.project if cli_configuration.project is not None else configuration.gitlab.project
    if _NAMESPACE_PROJECT_SEPARATOR not in project:
        project = f"{configuration.gitlab.namespace}{_NAMESPACE_PROJECT_SEPARATOR}{project}"

    gitlab_config = GitLabConfig(configuration.gitlab.url, configuration.gitlab.token)
    project_variables_manager = ProjectVariablesManager(gitlab_config, project)
    project_variables = project_variables_manager.get()

    return run_wrapped(cli_configuration.docker_args, project_variables, cli_configuration.interactive)


def main():
    """
    Main method.
    """
    cli_configuration = parse_cli_arguments(sys.argv[1:])
    returncode, stdout, stderr = run(cli_configuration)
    if stderr is not None:
        sys.stdout.write(stdout)
    if stderr is not None:
        sys.stderr.write(stderr)
    exit(returncode)


if __name__ == "__main__":
    main()
