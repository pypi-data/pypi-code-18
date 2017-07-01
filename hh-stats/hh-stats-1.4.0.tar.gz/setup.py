import setuptools
import re
import sys
import os.path

def _resolve_doc_link(project_path, match):
    with open(
        os.path.join(project_path, match.group('url')),
        encoding='utf-8',
    ) as doc_file:
        return '\n\n```json\n{:s}```'.format(doc_file.read())

_DOC_LINK_PATTERN = re.compile(r' \[(?P<url>docs/.*?)\]\((?P=url)\)\.')

if not (0x030500f0 <= sys.hexversion < 0x040000a0):
    raise Exception('requires Python >=3.5, <4.0')

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
    long_description = _DOC_LINK_PATTERN.sub(
        lambda match: _resolve_doc_link(project_path, match),
        readme_file.read(),
    )
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
    description='Utility for a collection of a vacancies stats ' \
        + 'from hh.ru service',
    long_description=long_description,
    license='MIT',
    author='thewizardplusplus',
    author_email='thewizardplusplus@yandex.ru',
    url='https://github.com/thewizardplusplus/' + project_name,
    packages=packages,
    install_requires=[
        'termcolor >=1.1.0, <2.0',
        'tzlocal >=1.4, <2.0',
        'parsedatetime >=2.4, <3.0',
        'pytimeparse >=1.1.6, <2.0',
        'jsonschema >=2.6.0, <3.0',
        'requests >=2.18.1, <3.0',
        'matplotlib >=2.0.2, <3.0',
    ],
    python_requires='>=3.5, <4.0',
    entry_points={
        'console_scripts': [
            '{:s} = {:s}:main'.format(project_name, package_name),
        ],
    },
)
