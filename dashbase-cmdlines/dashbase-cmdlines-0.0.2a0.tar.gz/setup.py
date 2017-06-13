from setuptools import setup
setup(
    name='dashbase-cmdlines',
    version='0.0.2-alpha',
    py_modules=['dashbase', 'cli', 'utils'],
    include_package_data=True,
    install_requires=[
        'texttable',
        'pyyaml',
        'click',
        'delegator.py',
        'tqdm',
        'requests',
        'psutil',
    ],
    entry_points='''
        [console_scripts]
        dashbase=cli.root:root
    ''',
)
