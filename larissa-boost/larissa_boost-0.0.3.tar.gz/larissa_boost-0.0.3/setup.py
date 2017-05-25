# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os, sys
from setuptools.command.install import install
import urllib2
import tarfile
import multiprocessing
import subprocess

here = os.path.abspath(os.path.dirname(__file__))

long_description = "See website for more info."

boost_name = "boost_1_64_0.tar.bz2"
boost_url = "https://dl.bintray.com/boostorg/release/1.64.0/source/" + boost_name

def find_file(file_name):
    """Locate the given file from our python root."""
    for root, dirs, files in os.walk(sys.prefix):
        if file_name in files:
            return root
    
    raise Exception("Cannot find file {0}".format(file_name))

def _install_boost():

    print("Downloading boost")
    # Download it
    response = urllib2.urlopen(boost_url)
    
    with open(boost_name,"wb") as f:
        f.write(response.read())

    response.close()
    print(os.system("ls -lah *"))

    # Extract the archive
    tar = tarfile.open(boost_name)
    tar.extractall()
    tar.close()
    print(os.system("ls -lah *"))

    # Find our new dir
    _, dirs, _ = next(os.walk("."))

    os.chdir(dirs[0])

    # Setup build
    try:
        print("Running command: ./bootstrap.sh --prefix={0}".format(os.path.join(sys.prefix,"boost")))
        print(subprocess.check_output("./bootstrap.sh --prefix={0}".format(os.path.join(sys.prefix,"boost")), shell=True))
    except Exception as e:
        raise Exception(e.output)

    # Build and install
    try:
        print("Running command: ./b2 install -j{0}".format(multiprocessing.cpu_count()))
        print(subprocess.check_output("./b2 install -j{0}".format(multiprocessing.cpu_count()), shell=True))
    except Exception as e:
        raise Exception(e.output)

    print(os.system("ls -la $VIRTUAL_ENV/"))
    print(os.system("ls -la $VIRTUAL_ENV/include/"))
    print(os.system("ls -la $VIRTUAL_ENV/boost/"))
    print(os.system("ls -la $VIRTUAL_ENV/boost/include"))

class CustomInstallCommand(install):
    """Need to custom compile boost."""
    def run(self):
        # Save off our dir
        cwd = os.getcwd()
        self.execute(_install_boost, (), msg='Compiling/Installing Boost')

        # Make sure we're in the right place
        os.chdir(cwd)
        install.run(self)

setup(
    name='larissa_boost',
    version='0.0.3',
    description='Boost library dependency building for larissa',
    long_description=long_description,
    url='https://github.com/owlz/larissa_boost',
    author='Michael Bann',
    author_email='self@bannsecurity.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console'
    ],
    keywords='libboost',
    packages=find_packages(exclude=['contrib', 'docs', 'tests','lib']),
    cmdclass={
        'install': CustomInstallCommand,
    },
)

