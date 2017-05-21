"""
Monkey-patching django.core.management functions
"""

import warnings

from django.core.management import *
from django.core import management as _core_management
from django.apps import apps


class CommandWarning(Warning):
    pass


_commands = None


def get_commands():
    global _commands
    if _commands is None:
        _commands = defaultdict(lambda: [])
        for name in find_commands(_core_management.__path__[0]):
            _commands[name].append('django.core')

        # Find the paths to the management modules
        paths = []
        for app_config in reversed(list(apps.get_app_configs())):
            paths.append((app_config.name,
                          os.path.join(app_config.path, 'management')))

        for app_name, path in paths:
            for name in find_commands(path):
                _commands[name].append(app_name)

    _core_management._commands = _commands
    return _commands

_core_management.get_commands = get_commands


def load_command_class(app_names, name):
    bases = []
    for app in reversed(app_names):
        module = import_module('%s.management.commands.%s' % \
                                               (app, name))
        # original command class
        app_cmd_class = module.Command

        add_cmd_class = True
        replaces_base = False
        for b in reversed(bases):
            if issubclass(app_cmd_class, b):
                # remove any base class of app_cmd_class already in the list
                bases.remove(b)
                replaces_base = True
            elif issubclass(b, app_cmd_class):
                # do not add the app_cmd_class if one of its subclasses
                # is already in the list
                add_cmd_class = False

        if add_cmd_class:
            bases.append(app_cmd_class)

    # easy case => no unnecessary subclassing
    if len(bases) == 1:
        return bases[0]()
    elif not bases:
        raise CommandError('Invalid command "%s"' % name)

    # check that all bases are subclasses of the same Command base class
    #  (LabelCommand or AppCommand)
    common_bases = list(bases[0].__mro__)
    for b in bases[1:]:
        for c in set(common_bases).difference(b.__mro__):
            common_bases.remove(c)

    if common_bases[0] == _core_management.BaseCommand:
        # the common base is the BaseCommand class. That means that there is
        # probably a command class inheritance conflict, as no command class
        # should directly inherit from BaseCommand
        warnings.warn(
             'Command "%s": Possible command classes inheritance conflict in '
             'apps %s. All command classes do not derive from the same django '
             'base class (AppCommand, LabelCommand, NoArgsCommand). This is '
             'likely to cause inconsistencies.' % (name, repr(app_names)),
             CommandWarning)

    # create Command class
    return type('Command', tuple(bases), {})()

_core_management.load_command_class = load_command_class


def main_help_text(self, commands_only=False):
    if commands_only:
        usage = sorted(get_commands().keys())
    else:
        usage = [
            "",
            "Type '%s help <subcommand>' for help on a specific subcommand." \
                % self.prog_name,
            "",
            "Available subcommands:",
        ]
        commands_dict = defaultdict(lambda: [])
        for name, apps in six.iteritems(get_commands()):
            for app in apps:
                if app == 'django.core':
                    app = 'django'
                else:
                    app = app.rpartition('.')[-1]
                commands_dict[app].append(name)
        style = color_style()
        for app in sorted(commands_dict.keys()):
            usage.append("")
            usage.append(style.NOTICE("[%s]" % app))
            for name in sorted(commands_dict[app]):
                usage.append("    %s" % name)
    return '\n'.join(usage)

_core_management.ManagementUtility.main_help_text = main_help_text
