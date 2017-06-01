import sys
import os
import json
import time
import datetime
# import test

# pylint: disable=invalid-name
PACKAGE = os.path.dirname(os.path.realpath(__file__))
HOME = os.path.expanduser('~')
TRASH = os.path.join(HOME, '.DeleteTrashBin')

def help():
    print("""For help:
    delete
    delete -help

Example usage:
    delete -settings
    delete -day [days]
    delete -size [size(G)]
    delete file1 file2 ...
    recover -list
    recover file1 file2 ...

Notes:
    File will be removed permanently after maximal days (infinite days in default).
    After trash bin size exceeds maximal size, older files will be removed (infinite size in default).
""")


def delete():
    args = sys.argv
    update()

    if len(args) == 1 or args[1] == '-help':
        help()
        return

    if args[1] == '-settings':
        settings()
        return

    if args[1] == '-day':
        change_day(args)
        return

    if args[1] == '-size':
        change_size(args)
        return

    if args[1][0] == '-':
        print('Unknown option')
        return
    else:
        for arg in args[1:]:
            if arg[-1] == '/' or arg[-1] == '\\':
                arg = arg[:-1]
            abs_path = os.path.abspath(arg)
            abs_dir = os.path.dirname(abs_path)
            basename = os.path.basename(arg)
            new_name = basename + '.' + str(time.time()).split('.')[0]
            try:
                os.rename(abs_path, os.path.join(TRASH, new_name))
            except OSError as e:
                print('File not found', abs_path)

def recover(args=None):
    args = sys.argv
    update()
    print('Recovering')


def update():
    pass


def change_day(args):
    print(args)

    if len(args) < 3:
        print('Invalid maximal size(G)')
        return

    try:
        maxday = int(args[2])
    except ValueError as e:
        print('Invalid maximal days')
        return

    if maxday <= 0:
        print('Invalid maximal days')
        return

    with open(os.path.join(PACKAGE, 'settings.txt'), 'r') as i_file:
        data = json.load(i_file)
    data['day'] = maxday
    with open(os.path.join(PACKAGE, 'settings.txt'), 'w') as o_file:
        json.dump(data, o_file, sort_keys=True, indent=4)
    return


def change_size(args):
    if len(args) < 3:
        print('Invalid maximal size(G)')
        return

    try:
        maxsize = int(args[2])
    except ValueError as e:
        print('Invalid maximal size(G)')
        return

    if maxsize <= 0:
        print('Invalid maximal size(G)')
        return

    with open(os.path.join(PACKAGE, 'settings.txt'), 'r') as i_file:
        data = json.load(i_file)
    data['size'] = maxsize
    with open(os.path.join(PACKAGE, 'settings.txt'), 'w') as o_file:
        json.dump(data, o_file, sort_keys=True, indent=4)
    return


def settings():
    with open(os.path.join(PACKAGE, 'settings.txt'), 'r') as io_file:
        data = json.load(io_file)
    print('Maximal days', data['day'])
    print('Maximal size', data['size'])