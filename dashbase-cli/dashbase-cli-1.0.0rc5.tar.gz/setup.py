import sys

from setuptools import setup, find_packages

if sys.version_info < (2, 7, 9):
    sys.exit('Sorry, Python < 2.7.9 is not supported')

setup(
    name='dashbase-cli',
    version='1.0.0rc5',
    url='http://www.dashbase.io',
    maintainer='wph95',
    maintainer_email='peter@dashbase.io',
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    install_requires=[
        'setuptools==36.0.1',
        'texttable==0.9.1',
        'pyyaml==3.12',
        'click==6.7',
        'colorama==0.3.9',
        'cryptography==1.9',
        'dateparser==0.6.0',
        'delegator.py==0.0.12',
        'tqdm==4.14.0',
        'requests==2.18.1',
        'urllib3==1.21.1',
        'paramiko==2.2.1',
        'psutil==5.2.2',
        'dateparser==0.6.0',
        'terminaltables==3.1.0',
    ],
    entry_points='''
        [console_scripts]
        dashbase-cli=dashbase.cli.cli:root
        dash=dashbase.tools.dbsql:main
        logtail=dashbase.tools.logtail:main
    ''',
    scripts=['dashbase-cli-completion.sh'],
)
