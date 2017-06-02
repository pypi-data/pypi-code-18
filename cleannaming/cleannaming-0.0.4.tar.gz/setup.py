try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='cleannaming',
    version='0.0.4',
    author='DmytryiStriletskyi',
    author_email='dmytryi.striletskyi@gmail.com',
    url='https://github.com/DmytryiStriletskyi/cleannaming',
    description='Clean your naming.',
    download_url='https://github.com/DmytryiStriletskyi/cleannaming.zip',

    py_modules=['cleannaming'],

    entry_points={
        'console_scripts': [
            'cleannaming = cleannaming:hello'
        ]
    },

    classifiers=[
        'Programming Language :: Python :: 3.5',
    ]
)
