try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='cleannaming',
    version='0.0.1',
    author='DmytryiStriletskyi',
    author_email='dmytryi.striletskyi@gmail.com',
    url='https://github.com/DmytryiStriletskyi/cleannaming',
    description='Clean your naming.',
    download_url='https://github.com/DmytryiStriletskyi/cleannaming.zip',

    packages=['cleannaming'],

    classifiers=[
        'Programming Language :: Python :: 3.5',
    ]
)
