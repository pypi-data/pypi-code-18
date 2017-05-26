import io
import os
from setuptools import setup
REQUIREMENTS_DIR = os.getcwd()
REQUIREMENTS_PATH = os.path.join(REQUIREMENTS_DIR, 'requirements.txt')

with io.open(REQUIREMENTS_PATH, 'r') as requirements:
    setup(
        name='ppg_common',
        version='1.54',
        description='Clients',
        url='https://bitbucket.org/sbg-interns/ppg_common',
        author='Sbg Core Interns',
        author_email='strahinja.kovacevic994@gmail.com',
        include_package_data=True,
        install_requires=[
            requirement[:-1] for requirement in requirements.readlines()
        ],
        packages=[
            'ppg_common',
            'ppg_common.errors',
            'ppg_common.clients',
            'ppg_common.handlers',
            'ppg_common.config'
        ]
    )
