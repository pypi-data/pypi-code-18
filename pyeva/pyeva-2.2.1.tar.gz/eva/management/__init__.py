import os
import sys
import logging
import importlib

from eva.conf import settings

CURDIR = os.path.dirname(os.path.realpath(__file__))


# cache
MAP_COMMANDS = {}


def exec_command_file(filepath):
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
    }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)
    return global_namespace.get('Command')


def _load_commands(cmdDir):

    LOCAL_COMMANDS = {}

    for f in os.listdir(cmdDir):
        if not f.endswith('.py'):
            continue

        if f.startswith('__'):
            continue

        cmdFile = os.path.join(cmdDir, f)
        Command = exec_command_file(cmdFile)

        if not Command:
            logging.warn('%s is not a Command Module!', cmdFile)
            continue

        c = Command()

        if not (hasattr(c, 'cmd') and
                hasattr(c, 'help') and
                hasattr(c, 'run')):
            logging.warn('%s is not a Command Module!',
                         os.path.join(CURDIR, f))
            continue

        LOCAL_COMMANDS[c.cmd] = c

    return LOCAL_COMMANDS


def load_commands():
    global MAP_COMMANDS

    if len(MAP_COMMANDS) != 0:
        return

    cmds = _load_commands(os.path.join(CURDIR, 'commands'))

    mod = importlib.import_module(settings.MANAGEMENT_MODULE)
    # TODO: _NamespacePath
    cmdDir = os.path.realpath(mod.__path__._path[0])
    cmds.update(_load_commands(cmdDir))

    MAP_COMMANDS['core'] = cmds


def print_usage():
    print('''{prog} - Eva Management Tools

Usage:

    {prog} NAMESPACE COMMAND OPTIONS

Help:

    {prog} help | -h | --help

Command:

'''.format(prog=sys.argv[0]))
    global MAP_COMMANDS
    for name in MAP_COMMANDS:
        print('[{0}]'.format(name))
        cmds = MAP_COMMANDS[name]
        for k in cmds:
            c = cmds[k]
            print('    {cmd:16} {help}'.format(cmd=c.cmd, help=c.help))
        print('')

    print('''
Example:

    # 同步/创建/初始化数据库
    {prog} core syncdb --db-echo

    # core 类型的 namespace 可以省略，因此上一条命令等于
    {prog} syncdb --db-echo
'''.format(prog=sys.argv[0]))


def main(argv=sys.argv[1:]):

    load_commands()

    if len(argv) < 1:
        print_usage()
        sys.exit(1)

    namespace = argv[0]

    # nice hack!
    if namespace.startswith('main') or namespace == 'core':
        if len(argv) < 2:
            print_usage()
            sys.exit(1)
        else:
            cmd = argv[1]
            argv = argv[2:] if len(argv) > 1 else []
    else:
        namespace = 'core'
        cmd = argv[0]
        argv = argv[1:] if len(argv) > 0 else []

    global MAP_COMMANDS

    if namespace in MAP_COMMANDS:
        cmds = MAP_COMMANDS[namespace]
        if cmd in cmds:
            cmds[cmd](argv)
            return

    if cmd in ['help', '-h', '--help']:
        print_usage()

    else:
        print('unknown cmd: ', cmd)
