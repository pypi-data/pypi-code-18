from os.path import expanduser
import sys
from pymj.builder import load_cython_ext
from pymj.generated import const


def discover_mujoco():
    # TODO: add paths based on export.
    """
    Discovers where MuJoCo is located in the file system.

    Returns:
    - mjpro_path (str): Path to MuJoCo Pro 1.50 directory.
    - key_path (str): Path to the MuJoCo license key.
    """
    if sys.platform in ["darwin", "linux"]:
        key_path = expanduser('~/.mujoco/mjkey.txt')
        mjpro_path = expanduser('~/.mujoco/mjpro150')
    else:
        key_path = expanduser('C:\mujoco\mjkey.txt')
        mjpro_path = expanduser('C:\mujoco\mjpro150')
    return (mjpro_path, key_path)


def user_warning_raise_exception(warn_bytes):

    '''
    User-defined warning callback, which is called by mujoco on warnings.
    Here we have two primary jobs:
        - Detect known warnings and suggest fixes (with code)
        - Decide whether to raise an Exception and raise if needed
    More cases should be added as we find new failures.
    '''
    # TODO: look through test output to see MuJoCo warnings to catch
    # and recommend. Also fix those tests
    warn = warn_bytes.decode()  # Convert bytes to string

    if 'Pre-allocated constraint buffer is full' in warn:
        raise Exception(warn + 'Increase njmax in mujoco XML')

    if 'Pre-allocated contact buffer is full' in warn:
        raise Exception(warn + 'Increase njconmax in mujoco XML')

    raise Exception('Got MuJoCo Warning: {}'.format(warn))

def user_warning_ignore_exception(warn_bytes):
    pass


class ignore_mujoco_warnings:
    """
    Class to turn off mujoco warning exceptions within a scope. Useful for
    large, vectorized rollouts.
    """
    def __enter__(self):
        self.prev_user_warning = cymj.get_warning_callback()
        cymj.set_warning_callback(user_warning_ignore_exception)
        return self

    def __exit__(self, type, value, traceback):
        cymj.set_warning_callback(self.prev_user_warning)


mjpro_path, key_path = discover_mujoco()
cymj = load_cython_ext(mjpro_path)

# Exposes all mj... functions from mujoco in pymj.functions..
class dict2(object):
    pass
functions = dict2()
for func_name in dir(cymj):
    if func_name.startswith("_mj"):
        setattr(functions, func_name[1:], getattr(cymj, func_name))

functions.mj_activate(key_path)
# Set user-defined callbacks that raise assertion with message
cymj.set_warning_callback(user_warning_raise_exception)

# Public API:
load_model_from_path = cymj.load_model_from_path
load_model_from_xml = cymj.load_model_from_xml
load_model_from_mjb = cymj.load_model_from_mjb
MjSim = cymj.MjSim
MjSimState = cymj.MjSimState
MjSimPool = cymj.MjSimPool
MjRenderContext = cymj.MjRenderContext
MjRenderContextWindow = cymj.MjRenderContextWindow
MjRenderContextOffscreen = cymj.MjRenderContextOffscreen


__all__ = ['MjSim', 'MjSimState', 'MjSimPool', 'MjRenderContext',
           'MjRenderContextWindow', 'MjRenderContextOffscreen',
           'load_model_from_path', 'load_model_from_xml', 'load_model_from_mjb',
           'ignore_mujoco_warnings', 'const', "functions"]


