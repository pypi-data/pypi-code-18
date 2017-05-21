from setuptools import setup, find_packages

setup(
    name='pyldr',
    version='0.1.2',
    modules=['script'],
    author='Zhan Lin',
    author_email='dy403164418@gmail.com',
    packages=find_packages(),
    license='MIT License',
    description='Python Package for Linear Decision Rule and Generalized Decision Rule',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy >= 1.11.3",
        "scipy >= 0.18.1",
    ],
)
