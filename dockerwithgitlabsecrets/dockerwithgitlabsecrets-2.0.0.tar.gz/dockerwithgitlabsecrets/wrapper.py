import logging
import os
import subprocess
from tempfile import NamedTemporaryFile

from typing import List, Tuple, Optional, Dict

_DOCKER_ENV_FILE_PARAMETER = "env-file"
_DOCKER_ENV_FILE_SUFFIX = ".env"
_DOCKER_BINARY = "docker"
_SUPPORTED_DOCKER_ACTIONS = ["run"]

_LINE_BREAK = "\n"
SAFE_LINE_BREAK = "\\n"

_ENCODING = "utf-8"

StdOutType = str
StdErrType = str
ReturnCodeType = int
ProgramOutputType = Tuple[ReturnCodeType, Optional[StdOutType], Optional[StdErrType]]

_logger = logging.getLogger(__name__)


def get_supported_action_index(docker_arguments: List[str]) -> Optional[int]:
    """
    Gets the index of the action to which 
    :param docker_arguments: 
    :return: 
    """
    if len(docker_arguments) == 0:
        return None

    docker_action_index = 0
    while docker_arguments[docker_action_index] not in _SUPPORTED_DOCKER_ACTIONS:
        docker_action_index += 1
        if docker_action_index == len(docker_arguments):
            return None
    return docker_action_index


def warn_if_new_lines_in_variables(variables: Dict[str, str]):
    """
    Emits a warning to the logger if one of the given key/value variables contains new line characters in its output.
    :param variables: the variables
    """
    for key, value in variables.items():
        if _LINE_BREAK in value:
            _logger.warning(f"New line characters in variable with key \"{key}\" have been escaped to \\\\n")


def run_wrapped(docker_arguments: List[str], variables: Dict[str, str], interactive: bool=False) -> ProgramOutputType:
    """
    Runs Docker with the given arguments with the given variables set in the envrionment.
    :param docker_arguments: the arguments to pass to Dcoker
    :param variables: the variables to set in the environment
    :param interactive: whether the wrapped Docker run should be interactive
    :return: the output of running Docker
    """
    docker_action_index = get_supported_action_index(docker_arguments)
    docker_call = [_DOCKER_BINARY]

    if docker_action_index is None:
        docker_call += docker_arguments
        process = subprocess.Popen(docker_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        returncode = process.returncode
    else:
        with NamedTemporaryFile(suffix=_DOCKER_ENV_FILE_SUFFIX, mode="w") as env_file:
            warn_if_new_lines_in_variables(variables)
            env_variables = os.linesep.join([f"{key}={value.replace(_LINE_BREAK, SAFE_LINE_BREAK)}"
                                             for key, value in variables.items()])
            env_file.write(env_variables)
            env_file.flush()

            docker_call += docker_arguments[0:docker_action_index+1] + \
                           [f"--{_DOCKER_ENV_FILE_PARAMETER}", env_file.name] \
                           + docker_arguments[docker_action_index+1:]

            if interactive:
                _logger.info("Running Docker in interactive mode")
                returncode = os.WEXITSTATUS(os.system(" ".join(docker_call)))
                return returncode, None, None
            else:
                process = subprocess.Popen(docker_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                returncode = process.returncode

    return returncode, stdout.decode(_ENCODING), stderr.decode(_ENCODING)
