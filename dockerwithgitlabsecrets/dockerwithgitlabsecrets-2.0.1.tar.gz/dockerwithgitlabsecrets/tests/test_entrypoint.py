import os
import re
import unittest
from tempfile import mkstemp

import yaml
from gitlab import Gitlab
from gitlabbuildvariables.common import GitLabConfig
from gitlabbuildvariables.manager import ProjectVariablesManager
from useintest.models import DockerisedServiceWithUsers
from useintest.predefined.gitlab import GitLab8_16_6_ce_0ServiceController
from useintest.services.controllers import DockerisedServiceController

from dockerwithgitlabsecrets.configuration import GITLAB_URL_PROPERTY, GITLAB_PROPERTY, GITLAB_TOKEN_PROPERTY, \
    GITLAB_PROJECT_PROPERTY, GITLAB_NAMESPACE_PROPERTY
from dockerwithgitlabsecrets.entrypoint import CliConfiguration, parse_cli_arguments, CONFIG_PARAMETER, \
    PROJECT_PARAMETER, is_interactive, run
from dockerwithgitlabsecrets.tests._common import EXAMPLE_PROJECT, EXAMPLE_LOCATION, EXAMPLE_DOCKER_ARGS, \
    EXAMPLE_VARIABLES

_CONFIG_PARAMETER_FLAG = f"--{CONFIG_PARAMETER}"
_PROJECT_PARAMETER_FLAG = f"--{PROJECT_PARAMETER}"

_GITLAB_PORT = 80


class TestParseCliArguments(unittest.TestCase):
    """
    Tests for `parse_cli_arguments`.
    """
    def test_parse_no_arguments(self):
        with self.assertRaises(SystemExit) as context:
            parse_cli_arguments([])
        # TODO: Capture stderr and check for help
        self.assertEqual(0, context.exception.code)

    def test_parse_only_config_location_argument(self):
        arguments = [_CONFIG_PARAMETER_FLAG, EXAMPLE_LOCATION]
        expected = CliConfiguration(config_location=EXAMPLE_LOCATION)
        self.assertEqual(expected, parse_cli_arguments(arguments))

    def test_parse_only_project_argument(self):
        arguments = [_PROJECT_PARAMETER_FLAG, EXAMPLE_PROJECT]
        expected = CliConfiguration(project=EXAMPLE_PROJECT)
        self.assertEqual(expected, parse_cli_arguments(arguments))

    def test_parse_program_arguments_with_docker_arguments(self):
        arguments = [_CONFIG_PARAMETER_FLAG, EXAMPLE_LOCATION, _PROJECT_PARAMETER_FLAG, EXAMPLE_PROJECT] \
                    + EXAMPLE_DOCKER_ARGS
        expected = CliConfiguration(project=EXAMPLE_PROJECT, config_location=EXAMPLE_LOCATION,
                                    docker_args=EXAMPLE_DOCKER_ARGS, interactive=True)
        self.assertEqual(expected, parse_cli_arguments(arguments))


class TestIsInteractive(unittest.TestCase):
    """
    Tests for `parse_cli_arguments`.
    """
    def test_without_flag(self):
        self.assertFalse(is_interactive(["run", "--rm", "ubuntu", "command"]))

    def test_with_interactive_flag(self):
        self.assertTrue(is_interactive(["run", "-t", "ubuntu"]))

    def test_with_interactive_flag_and_stdin_attach(self):
        self.assertTrue(is_interactive(["run", "-it", "ubuntu"]))

    def test_with_interactive_flag_and_stdin_attach_reversed(self):
        self.assertTrue(is_interactive(["run", "-ti", "ubuntu"]))


class TestRun(unittest.TestCase):
    """
    Tests for `run`.
    """
    _gitlab_service: DockerisedServiceWithUsers
    _gitlab_controller: DockerisedServiceController
    project_name: str
    gitlab_location: str
    gitlab_token: str

    @classmethod
    def setUpClass(cls):
        cls._gitlab_controller = GitLab8_16_6_ce_0ServiceController()
        cls._gitlab_service = cls._gitlab_controller.start_service()
        cls.gitlab_location = f"http://{cls._gitlab_service.host}:{cls._gitlab_service.ports[_GITLAB_PORT]}"

        gitlab = Gitlab(url=cls.gitlab_location, email=cls._gitlab_service.root_user.username,
                        password=cls._gitlab_service.root_user.password)
        gitlab.auth()

        cls.gitlab_token = gitlab.private_token
        cls.project_name = f"{cls._gitlab_service.root_user.username}/{EXAMPLE_PROJECT}"
        gitlab.projects.create({"name": EXAMPLE_PROJECT})

        project_variables_manager = ProjectVariablesManager(
            GitLabConfig(cls.gitlab_location, cls.gitlab_token), cls.project_name)
        project_variables_manager.set(EXAMPLE_VARIABLES)

    @classmethod
    def tearDownClass(cls):
        cls._gitlab_controller.stop_service(cls._gitlab_service)

    def setUp(self):
        _, self.configuration_location = mkstemp()
        with open(self.configuration_location, "w") as file:
            yaml.dump({
                GITLAB_PROPERTY: {
                    GITLAB_URL_PROPERTY: TestRun.gitlab_location,
                    GITLAB_TOKEN_PROPERTY: TestRun.gitlab_token,
                    GITLAB_PROJECT_PROPERTY: TestRun.project_name,
                    GITLAB_NAMESPACE_PROPERTY: TestRun.project_name.split("/")[0]
                }
            }, file)

    def tearDown(self):
        os.remove(self.configuration_location)

    def test_help(self):
        cli_configuration = CliConfiguration(docker_args=["--help"], config_location=self.configuration_location)
        return_code, stdout, stderr = run(cli_configuration)
        self.assertEqual(0, return_code)
        self.assertTrue(re.match("Usage:\sdocker", stdout.strip()))

    def test_run(self):
        key, value = list(EXAMPLE_VARIABLES.items())[0]
        cli_configuration = CliConfiguration(docker_args=["run", "--rm", "alpine", "printenv", key],
                                             config_location=self.configuration_location,
                                             project=TestRun.project_name.split("/")[1])
        return_code, stdout, stderr = run(cli_configuration)
        self.assertEqual(0, return_code)
        self.assertIn(value, stdout.strip())


if __name__ == "__main__":
    unittest.main()
