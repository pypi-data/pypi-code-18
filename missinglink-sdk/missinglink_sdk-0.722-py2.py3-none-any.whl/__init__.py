# coding=utf-8
import os
import sys
import logging
import ssl
from subprocess import Popen, PIPE
import os.path

from .sdk_version import get_version, get_keywords

loaded = False
__version__ = get_version()
keywords = get_keywords() or []
is_python2 = sys.version_info[0] == 2


def get_pip_server():
    pypi_server_hostname = 'testpypi' if 'test' in keywords else 'pypi'

    return 'https://{hostname}.python.org/pypi'.format(hostname=pypi_server_hostname)


def get_latest_pip_version():
    try:
        if is_python2:
            from xmlrpclib import ServerProxy, SafeTransport
        else:
            from xmlrpc.client import ServerProxy, SafeTransport

        if sys.version_info >= (2, 7, 9):
            context = None
            if hasattr(ssl, '_create_unverified_context'):
                context = ssl._create_unverified_context()

            transport = SafeTransport(use_datetime=True, context=context)
        else:
            transport = SafeTransport(use_datetime=True)

        pypi_server = get_pip_server()

        latest_version = ServerProxy(pypi_server, transport=transport).package_releases('missinglink-kernel')[0]

        return latest_version
    except Exception as e:
        logging.exception('could not check for new missinglink-sdk version:\n%s', str(e))
        return None


#  taken from python 3.3 source code
def which(cmd, mode=os.F_OK | os.X_OK, path=None):
    """Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.
    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.
    """
    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, mode):
        return (os.path.exists(fn) and os.access(fn, mode)
                and not os.path.isdir(fn))

    # If we're given a path with a directory part, look it up directly rather
    # than referring to PATH directories. This includes checking relative to the
    # current directory, e.g. ./script
    if os.path.dirname(cmd):
        if _access_check(cmd, mode):
            return cmd
        return None

    if path is None:
        path = os.environ.get("PATH", os.defpath)
    if not path:
        return None
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if not os.curdir in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for dir in path:
        normdir = os.path.normcase(dir)
        if not normdir in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name
    return None


def update_sdk(latest_version, user_path=False):
    pip_bin_path = which('pip')
    if pip_bin_path is None:
        python_bin_path = sys.executable
        pip_bin_path = os.path.join(os.path.dirname(python_bin_path), 'pip')
        if not os.path.exists(pip_bin_path):
            logging.warning("pip not found, can't self update missinglink sdk")
            return False

    require_package = 'missinglink-sdk==%s' % latest_version
    if user_path:
        args = (pip_bin_path, 'install', '--upgrade', '--user', '-i', get_pip_server(), require_package)
    else:
        args = (pip_bin_path, 'install', '--upgrade', '-i', get_pip_server(), require_package)

    try:
        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
        output, err = p.communicate()
    except Exception:
        logging.exception("%s failed", " ".join(args))
        return False

    rc = p.returncode

    if rc == 0:
        logging.info('MissingLink SDK updated to latest version (%s)', latest_version)
    else:
        logging.error('MissingLink SDK failed to upgrade to latest version (%s)', latest_version)
        logging.error("failed to run %s (%s)\n%s\n%s", " ".join(args), rc, err, output)

    return rc == 0


def self_update():
    global __version__

    if __version__ is None:
        __version__ = 'Please install this project with setup.py'
        return

    latest_version = get_latest_pip_version()

    if latest_version is None:
        return

    if str(__version__) == latest_version:
        return

    running_under_virtualenv = hasattr(sys, 'real_prefix')

    if running_under_virtualenv:
        update_sdk(latest_version)
    else:
        logging.info('updating missing link sdk to version %s in user path', latest_version)
        update_sdk(latest_version, user_path=True)


def do_import():
    import missinglink_kernel
    global __version__
    __version__ = missinglink_kernel.get_version()

    from missinglink_kernel import KerasCallback, TensorFlowCallback, \
        PyTorchCallback, PyCaffeCallback, ExperimentStopped

    return KerasCallback, TensorFlowCallback, PyTorchCallback, PyCaffeCallback, ExperimentStopped


if os.environ.get('MISSINGLINKAI_DISABLE_SELF_UPDATE') is not None:
    self_update()

KerasCallback, TensorFlowCallback, PyTorchCallback, PyCaffeCallback, ExperimentStopped, = do_import()


def debug_missinglink_on():
    logging.basicConfig()
    missinglink_log = logging.getLogger('missinglink')
    missinglink_log.setLevel(logging.DEBUG)
    missinglink_log.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    missinglink_log.addHandler(ch)


__all__ = [
    'KerasCallback',
    'TensorFlowCallback',
    'PyTorchCallback',
    'PyCaffeCallback',
    'debug_missinglink_on',
    'ExperimentStopped'
]
