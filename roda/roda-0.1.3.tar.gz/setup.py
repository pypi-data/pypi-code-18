from setuptools import setup, find_packages

setup(
    name='roda',
    version='0.1.3',
    packages=find_packages('src', exclude=['test']),

    install_requires=['nose'],
    author='x6doooo',
    author_email='x6doooo@gmail.com',
    description='...',
    license='MIT',
)
