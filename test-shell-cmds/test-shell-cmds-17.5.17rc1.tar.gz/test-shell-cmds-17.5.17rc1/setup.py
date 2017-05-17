from setuptools import setup
from setuptools.command.install import install
from subprocess import check_output


class _install(install):
    def run(self):
        cmd = ['uname', '-r']
        res = check_output(cmd)
        print('\n\n+++++ Tested %s\n\n' % (' '.join(cmd)))
        print('\n\n+++++ Result was: %s\n\n' % (res))


setup(name='test-shell-cmds',
      version='17.05.17rc1',
      cmdclass={
        'install': _install
      }
)
