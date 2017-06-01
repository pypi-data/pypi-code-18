from io import StringIO

import six

try:
    import configparser
except:
    from six.moves import configparser


class BlackDuckConfig(object):

    project_name = None
    project_version_name = None
    output_path = "build/blackduck"
    requirements_file_path = None
    ignore_failure = True

    section_name = "Black Duck Config"

    @classmethod
    def from_nothing(self):
        return BlackDuckConfig()

    @classmethod
    def from_file(self, config_file_path):
        config_str = None
        with open(config_file_path, "r") as config_file:
            config_str = config_file.read()
        return self.from_string(config_str)

    @classmethod
    def from_string(self, config_str, black_duck_config=None):
        bd_config = black_duck_config
        if bd_config is None:
            bd_config = self.from_nothing()

        string_buffer = None
        if six.PY2:
            string_buffer = StringIO(unicode(config_str))
        else:
            string_buffer = StringIO(config_str)

        config = configparser.RawConfigParser()
        config.allow_no_value = True
        config.readfp(string_buffer)

        """Initialize defaults"""
        output_path = bd_config.output_path
        requirements = bd_config.requirements_file_path
        i_fail = bd_config.ignore_failure

        project = bd_config.project_name
        version = bd_config.project_version_name

        """Parse config string"""
        output_path = bd_config.get(config, output_path, "OutputDirectory")
        requirements = bd_config.get(config, requirements, "RequirementsFile")
        i_fail = bd_config.getboolean(config, i_fail, "IgnoreFailure")

        project = bd_config.get(config, project, "Project-Name")
        version = bd_config.get(config, version, "Project-Version")

        bd_config.output_path = output_path
        bd_config.requirements_file_path = requirements
        bd_config.ignore_failure = i_fail

        bd_config.project_name = project
        bd_config.project_version_name = version

        clean(bd_config)
        return bd_config

    def get(self, config, default, property_name):
        value = None
        try:
            value = config.get(self.section_name, property_name)
        except configparser.NoOptionError:
            value = default
        return value

    def getboolean(self, config, default, property_name):
        value = None
        try:
            value = config.getboolean(self.section_name, property_name)
        except configparser.NoOptionError:
            value = default
        return value

    def getfloat(self, config, default, property_name):
        value = None
        try:
            value = config.getfloat(self.section_name, property_name)
        except configparser.NoOptionError:
            value = default
        return value


def clean(obj):
    if obj:
        for k, v in obj.__dict__.items():
            if v == "None":
                obj.__dict__[k] = None
