import os
import warnings


class RealEnvironment():
    def __init__(self):
        """
        Read .env file and set to shell environment.
        """
        try:
            content = [line.rstrip('\n') for line in open('.env')]
        except Exception as e:
            warnings.warn("Encountered error opening file.")
            return

        for line in content:
            try:
                os.environ[line.split(
                    '=')[0]] = line.split('=')[1]
            except:
                raise ValueError(
                    "Variable not defined to environment.Check the format")

    def get_env_or_default(self, key, default_value):
        """
        Get an environment variable from shell.

        Parameters
        ----------
        key : str
            Key is a name for variable
        default_value : str
            Default value for key

        Returns
        -------
        str
            Value from shell by key. If value is empty from shell,
            return default_value

        """
        try:
            return os.environ[key]
        except:
            return default_value

    def set_a_variable_to_environment(self, key, value):
        """
        Set an environment variable to shell.

        Parameters
        ----------
        key : str
            Key is a name for variable
        value : str
            Value for key
        """
        try:
            os.environ[key] = value
        except:
            raise ValueError(
                "Variable not defined to environment.Check the format")

    def remove_a_variable_from_environment(self, key):
        """
        Unset a variable
        """
        del os.environ[key]
