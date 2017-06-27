import os
import importlib
import subprocess

from setuptools import Command


class build_static(Command):
    user_options = []
    
    def run(self):
        package_name = self.distribution.packages[0]
        package_module = importlib.import_module(package_name)
        package_path = os.path.dirname(package_module.__file__)
        static_app_path = '{package_path}/static/{app_name}/'.format(
            package_path=package_path,
            app_name=package_name,
        )
        os.chdir(static_app_path)
        subprocess.run(['yarn', 'install', '--pure-lockfile'], check=True)
        subprocess.run(['yarn', 'run', 'compile'], check=True)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass
