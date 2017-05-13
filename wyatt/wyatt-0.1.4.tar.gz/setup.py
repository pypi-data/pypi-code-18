V='0.1.4'
from distutils.core import setup
from setuptools.command.install import install
import os, shutil, sys
print(os.getcwd())

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        DEST="/usr/local/bin/"
        DIR = self.install_lib
        os.system("touch ~/.bash_profile")
        os.system("echo 'export PATH=${PATH}:%swill/data/' >> ~/.bash_profile"%DIR)
        os.system('export PATH=${PATH}:%swill/data/'%DIR)
        header="#! %s"%sys.executable
        with open('%sget'%DIR, 'w+') as file:
            data=file.read()
            file.seek(0)
            file.write(header+data)
        with open('%ssend'%DIR, 'w+') as file:
            data=file.read()
            file.seek(0)
            file.write(header+data)

setup(name='wyatt',
      version=V,
      description='A way to talk to will wyatt.',
      author='wyatt',
      author_email='goFuck@your.self',
      url='https://iex.ist',
      packages=['will',],
      package_data={'will': ['data/*']},
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python',
          'Topic :: Communications :: Email',
                ],
      cmdclass={'install': PostInstallCommand,},
     )
