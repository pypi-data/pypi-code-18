import sys
import os
from setuptools import setup, find_packages
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        if sys.platform == "darwin":
            os.system('''echo 'eval "$(_CEREBRATE_COMPLETE=source cerebrate)"' >> ~/.profile''')
        elif sys.platform.startswith("linux"):
            os.system('''echo 'eval "$(_CEREBRATE_COMPLETE=source cerebrate)"' >> ~/.bashrc''')

        install.run(self)

setup(
    name='cerebrate',
    version='0.0.7',
    description='Offline Replay Manager for StarCraft II',
    author='Hugo Wainwright',
    author_email='wainwrighthugo@gmail.com',
    url='https://github.com/frugs/cerebrate',
    download_url='https://github.com/frugs/cerebrate/tarball/0.0.7',
    packages=find_packages(),
    py_modules=['cerebrate'],
    include_package_data=True,
    install_requires=[
        'tinydb',
        'click',
        'ujson'
    ],
    entry_points='''
        [console_scripts]
        cerebrate=cerebrate:cli
    ''',
    cmdclass={
        'install': PostInstallCommand,
    }
)