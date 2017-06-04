from setuptools import setup, find_packages

setup(
    name='roda',
    version='0.1.8',
    packages=find_packages(exclude=['test', 'test.*']),

    install_requires=['nose'],
    author='x6doooo',
    author_email='x6doooo@gmail.com',
    description='...',
    license='MIT',
)
