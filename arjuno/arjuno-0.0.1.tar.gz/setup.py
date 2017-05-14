import os
import sys
from distutils.sysconfig import get_python_lib
from setuptools import setup, find_packages
from arjuno.libs import version

overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "arjuno"))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break
try:
    long_description = open('README.md').read()
except:
    long_description = "serial SDK IOT"
    
setup (
    name='arjuno',
    version=version,
    url='https://github.com/rendiya/arjuno',
    author='rendiya',
    author_email='ligerrendy@gmail.com',
    description=('serial SDK IOT'),
    long_description = long_description,
    license='Apache2',
    packages=find_packages(),
    package_dir={'arjuno':'arjuno'},
    scripts=['arjuno/bin.py'],
    entry_points={'console_scripts': [
      'arjuno = arjuno.bin:bin',
    ]},
    include_package_data=True,
    install_requires=[
     'pyserial',
     'tornado'
  ],
    zip_safe = True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

if overlay_warning:
    sys.stderr.write("""
========
WARNING!
========
You have just installed astm_serial over top of an existing
installation, without removing it first. Because of this,
your install may now include extraneous files from a
previous version that have since been removed from
astm_serial. This is known to cause a variety of problems. You
should manually remove the
%(existing_path)s
directory and re-install astm_serial.
""" % {"existing_path": existing_path})