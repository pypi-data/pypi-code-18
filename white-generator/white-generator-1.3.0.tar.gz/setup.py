import setuptools
import re
import sys
import os.path

if not (0x030400f0 <= sys.hexversion < 0x040000a0):
    raise Exception('requires Python >=3.4, <4.0')

packages = setuptools.find_packages()
package_name = packages[0]
project_name = package_name.replace('_', '-')

project_path = os.path.dirname(os.path.abspath(__file__))
with open(
    os.path.join(project_path, package_name, 'consts.py'),
    encoding='utf-8',
) as consts_file:
    version = re.search(
        "^APP_VERSION = '([^']+)'$",
        consts_file.read(),
        re.MULTILINE,
    ).group(1)

with open(
    os.path.join(project_path, 'README.md'),
    encoding='utf-8',
) as readme_file:
    long_description = readme_file.read()
long_description = long_description[
    long_description.find('## Features')
    : long_description.find('## Screenshots')
].rstrip()
try:
    import pypandoc

    long_description = pypandoc.convert_text(long_description, 'rst', 'md')
except ImportError:
    pass

setuptools.setup(
    name=project_name,
    version=version,
    description='Utility for a generation of memes',
    long_description=long_description,
    license='MIT',
    author='thewizardplusplus',
    author_email='thewizardplusplus@yandex.ru',
    url='https://github.com/thewizardplusplus/' + project_name,
    packages=packages,
    install_requires=[
        'termcolor >=1.1.0, <2.0',
        'pillow >=4.1.1, <5.0',
    ],
    python_requires='>=3.4, <4.0',
    entry_points={
        'console_scripts': [
            '{:s} = {:s}:main'.format(project_name, package_name),
        ],
    },
)
