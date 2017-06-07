import sys
import argparse
import importlib
from . import settings


def run():
    """Main entry point to the Resyndicator."""
    parser = argparse.ArgumentParser(description='Run Resyndicator command.')
    parser.add_argument('-s', '--settings', required=True,
                        help='The settings module')
    parser.add_argument('command', help='The command')
    args, rest = parser.parse_known_args(sys.argv[1:])
    app_settings = importlib.import_module(args.settings)
    package = args.settings.rsplit('.', 1)[0]
    settings.RESOURCES = package + '.resources'
    for key, value in vars(app_settings).items():
        if not key.startswith('_'):
            setattr(settings, key, value)
    settings.BASE_COMMANDS.update(settings.COMMANDS)
    if args.command in settings.BASE_COMMANDS:
        module_name, function_name = \
            settings.BASE_COMMANDS[args.command].rsplit('.', 1)
        module = importlib.import_module(module_name)
        function = getattr(module, function_name)
        return function(rest)
    else:
        print('Valid commands (call <command> --help for help):')
        print('\n'.join(settings.COMMANDS.keys()))


if __name__ == '__main__':
    run()
