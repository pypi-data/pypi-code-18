__version__ = '0.5.1'

class Storage(object):
    """
    An abstaction for reading and writing sheets from
    and to long term storage.
    """
    def get_object(self, object_id):
        raise NotImplementedError()

    def save_object(self, object_id, object_):
        raise NotImplementedError()

class StorageProxy(object):
    """
    This class is an abstraction for indirect access to a Storage object.
    """
    def get_object(self, object_id):
        raise NotImplementedError()

    def save_object(self, object_id, object_):
        raise NotImplementedError()

import argparse
import asyncio
import logging
import logging.config
import modconf

logger = logging.getLogger(__name__)

import ws_storage.server
import ws_storage.filesystem

def runserver(args):
    try:
        ws_storage.server.runserver(args)
    except Exception as e:
        logger.exception(str(e))

def install(args):
    # copy systemd file
    shutil.copyfile(
            os.path.join(BASE_DIR, 'ws_storage.service'),
            os.path.join('/lib/systemd/system', 'ws_storage.service'))

    config_dir_dst = '/etc/ws_storage/conf'

    # make etc directory
    try:
        os.makedirs(config_dir_dst)
    except: pass
    
    # copy default config file
    shutil.copyfile(
            os.path.join(BASE_DIR, 'tests/conf/simple.py'),
            os.path.join(config_dir_dst, 'simple.py'))
    shutil.copyfile(
            os.path.join(BASE_DIR, 'tests/conf/simple_console.py'),
            os.path.join(config_dir_dst, 'simple_console.py'))

def main(argv):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    parser_runserver = subparsers.add_parser('runserver')
    parser_runserver.add_argument(
            '-d',
            action='store_true',
            help='develop mode',
            )
    parser_runserver.add_argument(
            '--conf_dir',
            nargs=1,
            default=(None,),
            help='modconf module directory',
            )
    parser_runserver.add_argument(
            'conf_mod',
            help='modconf module name',
            )
    
    parser_runserver.set_defaults(func=runserver)
 
    parser_install = subparsers.add_parser('install')
    parser_install.set_defaults(func=install)

    args = parser.parse_args(argv[1:])
    args.func(args)







