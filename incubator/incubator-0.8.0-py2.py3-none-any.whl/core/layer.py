import os

from .constants import COMMIT_MESSAGE_START


class ImageLayer(object):
    """
    Represent one layer in final image.

    Contains commands and configuration for this layer.
    """

    def __init__(self, number, global_context, commands=None):
        self._commands = commands or []
        self.number = number
        self.is_last = False
        self.commit_message = COMMIT_MESSAGE_START
        self.context = LayerContext(global_context=global_context)

    def __str__(self):
        commands = "["
        for cmd in self.commands:
            commands += "<{}>".format(str(cmd))
        commands += "]"
        return "layer {}: {}".format(str(self.number), commands)

    def add_command(self, command, content):
        self._commands.append(command)

        formated_content = " {}".format(content.rstrip())
        self.commit_message += formated_content
        label_name = "layer_{}_commands".format(str(self.number))

        self.context.labels.setdefault(label_name, "")
        self.context.labels[label_name] += formated_content

    @property
    def commands(self):
        return self._commands


class LayerContext(object):
    """
    Represent context and configuration of one layer.

    Contains metadata and commit config for new layer.
    """

    def __init__(self, global_context):
        self.global_context = global_context
        self.container = None
        self.author = None
        self.labels = {}

        self._envs = {}
        self._logs = []

        self._commit_config_properties = {}

    def add_commit_property(self, key, value):
        self._commit_config_properties[key] = value

    def add_commit_property_to_subdict(self, subdict, key, value):
        self._commit_config_properties.setdefault(subdict, {})
        self._commit_config_properties[subdict][key] = value

    def update_labels(self, labels):
        self.labels.update(labels)

    def update_envs(self, envs):
        self.global_context.envs.update(envs)
        self._envs.update(envs)

    def use_buildarg(self, key, value):
        self.global_context.use_buildarg(key, value)

    def add_log(self, log):
        self._logs.append(log)

    def change_workdir(self, workdir):
        new_workdir = os.path.normpath(os.path.join(self.global_context.workdir, workdir))
        self.add_commit_property("WorkingDir", new_workdir)
        self.global_context.workdir = new_workdir

    @property
    def commit_config(self):
        """
        Read-only property which can be used as a commit-config dictionary
        on container commit.

        :return: dict as a commit-config for this layer
        """
        config = dict(self._commit_config_properties)

        config.setdefault("Env", [])
        for k, v in self._envs.items():
            config["Env"].append('{}={}'.format(str(k), str(v)))

        config.setdefault("Labels", {})
        config["Labels"].update(self.labels)

        return config

    @property
    def logs(self):
        return self._logs
