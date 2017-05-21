from distutils.core import setup

setup(
    name='pyldr',
    version='0.1.1',
    py_modules='script'
    author='Zhan Lin',
    author_email='dy403164418@gmail.com',
    packages=['pyldr'],
    license='LICENSE.txt',
    description='Python Package for Linear Decision Rule and Generalized Decision Rule',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy >= 1.11.3",
        "scipy >= 0.18.1",
    ],
)
