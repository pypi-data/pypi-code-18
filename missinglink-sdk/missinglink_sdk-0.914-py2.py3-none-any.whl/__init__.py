# coding=utf-8
import sys
import logging
import os.path
from .sdk_version import get_version, get_keywords
from .pip_util import get_latest_pip_version, pip_install, get_pip_server

loaded = False
__version__ = get_version()
keywords = get_keywords() or []


# noinspection PyBroadException
def update_sdk(latest_version, user_path, throw_exception):
    require_package = 'missinglink-sdk==%s' % latest_version
    p, args = pip_install(get_pip_server(keywords), require_package, user_path)

    if p is None:
        return False

    try:
        std_output, std_err = p.communicate()
    except Exception:
        if throw_exception:
            raise

        logging.exception("%s failed", " ".join(args))
        return False

    rc = p.returncode

    if rc != 0:
        logging.error('MissingLink SDK failed to upgrade to latest version (%s)', latest_version)
        logging.error("failed to run %s (%s)\n%s\n%s", " ".join(args), rc, std_err, std_output)
        return False

    logging.info('MissingLink SDK updated to latest version (%s)', latest_version)

    return True


def self_update(throw_exception=False):
    global __version__

    version = get_version()

    if version is None:
        __version__ = 'Please install this project with setup.py'
        return

    latest_version = get_latest_pip_version(keywords, throw_exception=throw_exception)

    if latest_version is None:
        return

    if str(version) == latest_version:
        return

    running_under_virtualenv = getattr(sys, 'real_prefix', None) is not None

    if not running_under_virtualenv:
        logging.info('updating missing link sdk to version %s in user path', latest_version)

    return update_sdk(latest_version, user_path=not running_under_virtualenv, throw_exception=throw_exception)


def do_import():
    import missinglink_kernel

    global __version__
    __version__ = missinglink_kernel.get_version()

    from missinglink_kernel import KerasCallback, TensorFlowCallback, \
        PyTorchCallback, PyCaffeCallback, ExperimentStopped

    return KerasCallback, TensorFlowCallback, PyTorchCallback, PyCaffeCallback, ExperimentStopped


def self_update_if_not_disabled():
    if os.environ.get('MISSINGLINKAI_DISABLE_SELF_UPDATE') is None:
        self_update()


self_update_if_not_disabled()

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
