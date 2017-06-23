import argparse
import os
import sys
from subprocess import check_output

from . import utils

_is_verbose = False
parser = None

CONF_FILES = (
    '_BACKUP_THIS',
    '.BACKUP_THIS',
)


def parse_args(argv):
    global parser
    parser = argparse.ArgumentParser(
        prog='bupper',
        description='Simple backup script, no diffing or anything fancy.'
    )

    source_dir = os.environ.get('BUPPER_SOURCE', '~')
    local_dir = os.environ.get('BUPPER_LOCAL_BACKUP', '/var/tmp/bupper/')
    remote_dir = os.environ.get('BUPPER_REMOTE_BACKUP', None)

    parser.add_argument('-d', '--date-format', help='date format in strftime',
                        default='ISO')
    parser.add_argument('-v', '--verbose', help='increase output verbosity',
                        action='store_true')
    parser.add_argument('-s', '--source', help='source directory to '
                        ' scan for bupper configs', default=source_dir)
    parser.add_argument('-l', '--local', help='local storage of backups',
                        default=local_dir)
    parser.add_argument('-r', '--remote', help='remote storage of backups',
                        default=remote_dir)
    args = parser.parse_args(argv)
    return args


def get_targets(path):
    '''
    Walk a directory structure and of full paths to all buppable roots
    '''
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename in CONF_FILES:
                yield dirpath


def check_args(args):
    '''
    Raises value errors if args is missing something
    '''
    if args.verbose:
        global _is_verbose
        _is_verbose = True
    # Expand all relevant user directories
    args.source = os.path.expanduser(args.source)
    args.local = os.path.expanduser(args.local)


def do_backup(args, path):
    # Create local archive
    filename = utils.get_backup_archive_filename(args.date_format, path)
    local_path = os.path.join(args.local, filename)
    if not os.path.exists(local_path):
        do_local(path, local_path)

    # Record a "reverse" link in the MD5s
    md5 = gen_md5(local_path)
    md5_path = os.path.join(args.local, md5)
    mode = 'a' if os.path.exists(md5_path) else 'w+'
    open(md5_path, mode).write('%s\n' % filename)
    # TODO check if MD5 exists in remote

    # Send the backup to the remote host, if necessary
    if args.remote:
        do_scp(local_path, args.remote)
        # TODO add confirmation file here


def gen_md5(local_path):
    output_bytes = check_output(['md5sum', local_path])
    output_string = output_bytes.decode()
    checksum = output_string.strip().split(' ')[0].strip()
    if _is_verbose:
        print('Checksum for %s: %s' % (local_path, checksum))
    return checksum


def do_local(source_path, local_path):
    args = '-czf'
    if _is_verbose:
        print('Generating tar.gz "%s" -> "%s"' % (source_path, local_path))
        args = '-cvzf'
    utils.makedirs_to(local_path)
    output = check_output(['tar', args, local_path, source_path])
    if _is_verbose:
        print('TAR ----\n%s\n----\n' % output)


def do_scp(local, remote):
    if _is_verbose:
        print('Transfering "%s" -> "%s"' % (local, remote))
    output = check_output(['scp', local, remote])
    if _is_verbose:
        print('SCP ----\n%s\n----\n' % output)


def main(args):
    try:
        check_args(args)
    except ValueError:
        parser.print_usage()
        sys.exit(1)

    all_dirs = utils.without_duplicates(get_targets(args.source))
    for buppable in all_dirs:
        do_backup(args, buppable)


def cli():
    main(parse_args(sys.argv))


if __name__ == '__main__':
    cli()
