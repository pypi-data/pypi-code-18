V='0.1.9'
from distutils.core import setup
from setuptools.command.install import install
import os, shutil, sys
from os.path import expanduser
home = expanduser("~")

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        DEST="/usr/local/bin/"
        DIR = self.install_lib+"will/data/"
        export='export PATH=${PATH}:%s'%DIR
        print("Opening %s"%"%s/.bash_profile"%home)
        with open("%s/.bash_profile"%home, "r+") as file:
            data = file.read()
            if export not in data:
                file.seek(0)
                file.write(data + export)
        os.environ["PATH"]='%s:%s'%(os.environ["PATH"],DIR)
        header="#! %s"%sys.executable
        print("Opening %s."%'%sget'%DIR)
        with open('%sget'%DIR, 'r+') as file:
            data=file.read()
            file.seek(0)
            print("The data in this file: %s"%data)
            file.write(header+data)
            print("Sucessfully wrote to get.")
        print("Opening %s."%'%ssend'%DIR)
        with open('%ssend'%DIR, 'r+') as file:
            data=file.read()
            file.seek(0)
            file.write(header+data)
            print("Sucessfully wrote to send.")

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
