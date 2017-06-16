import os
import sys

# directories
MODRPC_ROOT_DIR = ''
MODRPC_TMP_DIR = ''
MODPY_ROOT_DIR = ''
MODPY_ETC_DIR = ''
MODPY_NODE_DIR = ''


def remove_trailing_slash(path):
    if path.endswith('/'):
        path = path[:-1]
    return path

_init_done = False
def init():
    global _init_done
    global MODRPC_ROOT_DIR
    global MODRPC_TMP_DIR
    global MODPY_ROOT_DIR
    global MODPY_NODE_DIR
    global MODPY_ETC_DIR
    if (_init_done):
        return
    _init_done = True

    # MODRPCROOT
    mrpcroot = os.getenv('MODRPCROOT')
    if mrpcroot != None:
        if (not os.path.exists(mrpcroot)):
            print('MODRPCROOT (%s) does not exist.' % mrpcroot)
            sys.exit()
        if (not os.path.isdir(mrpcroot)):
            print('MODRPCROOT (%s) must be a directory.' % mrpcroot)
            sys.exit()
        MODRPC_ROOT_DIR = remove_trailing_slash(mrpcroot)

    # MODPYROOT
    modpyroot = os.getenv('MODPYROOT')
    if modpyroot != None:
        if (not os.path.exists(modpyroot)):
            print('MODPYROOT (%s) does not exist.' % modpyroot)
            sys.exit()
        if (not os.path.isdir(modpyroot)):
            print('MODPYROOT (%s) must be a directory.' % modpyroot)
            sys.exit()
        MODPY_ROOT_DIR = remove_trailing_slash(modpyroot)
    elif MODRPC_ROOT_DIR != '':
        MODPY_ROOT_DIR = MODRPC_ROOT_DIR + '/py'
    else:
        print('Either MODRPCROOT or MODPYROOT environment variable must be set.')
        sys.exit()

    MODPY_ETC_DIR = MODPY_ROOT_DIR + '/etc'
    MODPY_NODE_DIR = MODPY_ROOT_DIR + '/nodes'
    if not os.path.exists(MODPY_ETC_DIR):
        os.makedirs(MODPY_ETC_DIR)
    if not os.path.exists(MODPY_NODE_DIR):
        os.makedirs(MODPY_NODE_DIR)

    # MODRPCTMP
    mrpctmp = os.getenv('MODRPCTMP')
    if (mrpctmp != None):
        MODRPC_TMP_DIR = remvoe_trailing_slash(mrpctmp)
    else:
        MODRPC_TMP_DIR = '/var/tmp/modrpc'
    if not os.path.exists(MODRPC_TMP_DIR):
        os.makedirs(MODRPC_TMP_DIR)

def get_etc_dir():
    return MODPY_ETC_DIR

def get_node_dir():
    return MODPY_NODE_DIR

def get_tmp_dir():
    return MODRPC_TMP_DIR
