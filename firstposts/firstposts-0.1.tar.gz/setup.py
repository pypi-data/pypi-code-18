from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='firstposts',
    version='0.1',
    description='Find Subreddit Firstposts',
    long_description=long_description,
    url='https://github.com/gusberinger/firstposts',
    author='Gus Beringer',
    author_email='gusberinger@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Internet'
    ],
    keywords='reddit',
    packages=find_packages(exclude=['config.yml']),
    install_requires=['pyYAML', 'praw'],
    scripts=['firstposts/firstposts.py']
)
