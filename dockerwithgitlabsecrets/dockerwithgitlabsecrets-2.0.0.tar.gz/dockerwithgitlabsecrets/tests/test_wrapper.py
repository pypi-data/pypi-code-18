import unittest
from tempfile import NamedTemporaryFile

from dockerwithgitlabsecrets.tests._common import EXAMPLE_VALUE, EXAMPLE_PARAMETER, EXAMPLE_VARIABLES
from dockerwithgitlabsecrets.wrapper import run_wrapped, SAFE_LINE_BREAK


class TestWrapper(unittest.TestCase):
    """
    Tests for `run_wrapped`.
    """
    def test_help_with_docker_command(self):
        return_code, stdout, stderr = run_wrapped(["ps", "--help"], EXAMPLE_VARIABLES)
        self.assertEqual(0, return_code)
        self.assertIn("Usage:\tdocker ps", stdout.strip())

    def test_with_non_supported_action(self):
        return_code, stdout, stderr = run_wrapped(["version"], EXAMPLE_VARIABLES)
        self.assertEqual(0, return_code)
        self.assertIn("Version", stdout.strip())

    def test_has_standard_variable(self):
        return_code, stdout, stderr = run_wrapped(
            ["run", "-e", f"{EXAMPLE_PARAMETER}={EXAMPLE_VALUE}", "--rm", "alpine", "printenv", EXAMPLE_PARAMETER],
            EXAMPLE_VARIABLES)
        self.assertEqual(0, return_code)
        self.assertEqual(EXAMPLE_VALUE, stdout.strip())

    def test_run_has_secret_variable(self):
        key, value = list(EXAMPLE_VARIABLES.items())[0]
        return_code, stdout, stderr = run_wrapped(["--debug", "run", "--rm", "alpine", "printenv", key],
                                                  EXAMPLE_VARIABLES)
        self.assertEqual(0, return_code)
        self.assertEqual(value, stdout.strip())

    def test_run_has_multiline_secret_variable(self):
        key, value = list(EXAMPLE_VARIABLES.items())[1]
        return_code, stdout, stderr = run_wrapped(["run", "--rm", "alpine", "printenv", key],
                                                  EXAMPLE_VARIABLES)
        self.assertEqual(0, return_code)
        self.assertEqual(value.replace("\n", SAFE_LINE_BREAK), stdout.strip())

    def test_run_cli_variable_has_higher_precedence(self):
        other_value = "other-value"
        key, value = list(EXAMPLE_VARIABLES.items())[0]
        return_code, stdout, stderr = run_wrapped(["run", "-e", f"{key}={other_value}", "--rm", "alpine", "printenv",
                                                   key], EXAMPLE_VARIABLES)
        self.assertEqual(0, return_code)
        self.assertEqual(other_value, stdout.strip())

    def test_run_with_env_file(self):
        key, value = list(EXAMPLE_VARIABLES.items())[0]
        key_2, value_2 = list(EXAMPLE_VARIABLES.items())[2]
        example_override = "override"

        with NamedTemporaryFile("w") as env_file:
            env_file.write(f"{key}={example_override}")
            env_file.flush()
            return_code, stdout, stderr = run_wrapped(
                ["run", "--env-file", f"{env_file.name}", "--rm", "alpine", "printenv", key], EXAMPLE_VARIABLES)
            self.assertEqual(0, return_code)
            self.assertEqual(example_override, stdout.strip())

            return_code, stdout, stderr = run_wrapped(
                ["run", "--env-file", f"{env_file.name}", "--rm", "alpine", "printenv", key_2], EXAMPLE_VARIABLES)
            self.assertEqual(0, return_code)
            self.assertEqual(value_2, stdout.strip())

    def test_run_in_interactive_mode(self):
        key, value = list(EXAMPLE_VARIABLES.items())[0]
        return_code, stdout, stderr = run_wrapped(["run", "--rm", "-t", "alpine", "printenv", key], EXAMPLE_VARIABLES,
                                                  interactive=True)
        self.assertEqual(0, return_code)


if __name__ == "__main__":
    unittest.main()
