import logging
import os
import tarfile

from .constants import APP_NAME
from .fileutils import (copy_files_to_container, create_directory,
                        norm_path_with_work_dir, put_archive)
from .layer import ImageLayer
from .output import CHAPTER, ERROR_SUBTITLE
from .parsing import apply_shell_expansion, substitute_variables
from .utilclasses import CommandLog

logger = logging.getLogger(APP_NAME)


class Command:
    def __init__(self, value, content,
                 line_envs, line_labels):
        self.value = value
        self._content = content
        self._line_envs = line_envs
        self._line_labels = line_labels

    @staticmethod
    def changes_data():
        pass

    @staticmethod
    def raw_value():
        return False

    def apply(self, client, layer_context, build_context, config):
        pass

    def __str__(self):
        return "{} {}".format(self.__class__.__name__, self.value)

    def __call__(self, client, layer_context, build_context, config):
        logger.info(CHAPTER.format(self._content))
        self.value = substitute_variables(s=self.value,
                                          variables=layer_context.global_context.envs)

        if not self.raw_value():
            self.value = apply_shell_expansion(self.value)
        self.apply(client=client,
                   layer_context=layer_context,
                   build_context=build_context,
                   config=config)


class Arg(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, layer_context, build_context, config):
        value_split = self.value.split('=', 1)

        if len(value_split) == 1:
            key, default_value = value_split[0], ""
        elif len(value_split) == 2:
            key, default_value = value_split
        else:
            raise Exception("Wrong format of ARG command.")

        layer_context.use_buildarg(key=key,
                                   value=config.buildargs.get(key, default_value))


class Copy(Command):
    @staticmethod
    def changes_data():
        return True

    def apply(self, client, layer_context, build_context, config):
        splited_command = self.value.split()
        if len(splited_command) < 2:
            logger.warning('Wrong command: {}'.format(str(self.value)))
            return
            # exception?

        source_files = splited_command[0:-1:]
        target_path = norm_path_with_work_dir(path=splited_command[-1],
                                              workdir=layer_context.global_context.workdir)
        copy_files_to_container(container=layer_context.current_container,
                                client=client,
                                config=config,
                                context=build_context,
                                source=source_files,
                                target=target_path)


class Add(Command):
    @staticmethod
    def changes_data():
        return True

    def apply(self, client, layer_context, build_context, config):
        splited_command = self.value.split()
        if len(splited_command) < 2:
            logger.warning('Wrong command: {}'.format(str(self.value)))
            return
            # exception?

        source_files = splited_command[0:-1:]
        target_path = norm_path_with_work_dir(path=splited_command[-1],
                                              workdir=layer_context.global_context.workdir)

        for src in source_files:
            file = build_context.get_file(src)
            if file:
                try:
                    with tarfile.open(fileobj=file):
                        put_archive(client=client,
                                    config=config,
                                    container=layer_context.current_container,
                                    tar=file,
                                    target=target_path)
                        break
                except:
                    pass
            copy_files_to_container(container=layer_context.current_container,
                                    client=client,
                                    config=config,
                                    context=build_context,
                                    source=[src],
                                    target=target_path)


class Cmd(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, layer_context, build_context, config):
        layer_context.add_commit_property("Cmd", self.value)


class Entrypoint(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, layer_context, build_context, config):
        layer_context.add_commit_property("Entrypoint", self.value)


class Env(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, layer_context, build_context, config):
        layer_context.update_envs(self._line_envs)


class Expose(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, layer_context, build_context, config):
        ports = self.value.split(" ")
        for p in ports:
            layer_context.add_commit_property_to_subdict("ExposedPorts", p, {})


class From(Command):
    @staticmethod
    def changes_data():
        return False


class Label(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, layer_context, build_context, config):
        layer_context.update_labels(self._line_labels)


class Maintainer(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, layer_context, build_context, config):
        layer_context.author = self.value


class Run(Command):
    @staticmethod
    def changes_data():
        return True

    @staticmethod
    def raw_value():
        return True

    def apply(self, client, layer_context, build_context, config):

        command = self.value
        log = CommandLog(command=self._content)

        if layer_context.global_context.workdir and layer_context.global_context.workdir != os.curdir:
            command = "cd {}; {}".format(layer_context.global_context.workdir, command)

        for l in client.execute(container=layer_context.current_container,
                                cmd=command,
                                envs=layer_context.global_context.envs):
            logger.debug(str(l.decode().rstrip()))
            log.add_log(l)
        logger.debug("")


class StopSignal(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, layer_context, build_context, config):
        layer_context.add_commit_property("StopSignal", self.value)


class User(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, layer_context, build_context, config):
        layer_context.add_commit_property("User", self.value)


class Volume(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, layer_context, build_context, config):
        volumes = self.value.split(" ")
        for v in volumes:
            layer_context.add_commit_property_to_subdict("Volumes", v, {})


class Workdir(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, layer_context, build_context, config):
        layer_context.change_workdir(self.value)
        create_directory(client=client,
                         config=config,
                         container=layer_context.current_container,
                         target=layer_context.global_context.workdir)


COMMANDS = {
    "ADD": Add,
    "ARG": Arg,
    "CMD": Cmd,
    "COPY": Copy,
    "ENTRYPOINT": Entrypoint,
    "ENV": Env,
    "EXPOSE": Expose,
    "FROM": From,
    "LABEL": Label,
    "MAINTAINER": Maintainer,
    "RUN": Run,
    "STOPSIGNAL": StopSignal,
    "USER": User,
    "VOLUME": Volume,
    "WORKDIR": Workdir
}


def _get_layer_split_marks(layers, instruction_count):
    layers_split_mark = layers
    if layers_split_mark is None or layers_split_mark == []:
        layers_split_mark = [i for i in range(instruction_count)]

    if layers_split_mark[-1] != instruction_count:
        layers_split_mark.append(instruction_count)

    logger.debug(CHAPTER.format("layer splits: {}".format(layers_split_mark)))

    for l in layers_split_mark:
        if l > instruction_count:
            raise Exception("Layer split {} is bigger then number of instructions ({})."
                            .format(l, instruction_count))
    return layers_split_mark


def get_layers_from_dockerfile_structure(structure, env_label_context, layers, global_context):
    layers_split_mark = _get_layer_split_marks(layers=layers,
                                               instruction_count=len(structure))

    layers = []
    current_command = 0
    layer_number = 1
    data_changed = False

    layer = ImageLayer(number=0,
                       global_context=global_context)

    for layer_split in layers_split_mark:

        for i in range(current_command, layer_split):
            cmd = structure[i]
            context = env_label_context[i]

            instruction = cmd["instruction"]
            cmdType = COMMANDS.get(instruction)
            if not cmdType:
                logger.warning(ERROR_SUBTITLE.format("Unknown instruction {}.".format(instruction)))
            else:
                layer.add_command(command=cmdType(value=cmd["value"],
                                                  content=cmd['content'],
                                                  line_envs=context.line_envs,
                                                  line_labels=context.line_labels),
                                  content=cmd['content'])

                current_command += 1
                data_changed = data_changed or cmdType.changes_data()

        if data_changed or layer_split == len(structure):
            data_changed = False
            layers.append(layer)
            if not layer_split == len(structure):
                layer = ImageLayer(number=layer_number,
                                   global_context=global_context)
                layer_number += 1
            else:
                layer.is_last = True

    return layers
