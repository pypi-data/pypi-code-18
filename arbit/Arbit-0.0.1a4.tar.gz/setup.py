from setuptools import setup, find_packages

setup(
    name="Arbit",
    version="0.0.1a4",
    python_requires='>=3',
    author='Tjaden Hess',
    author_email='tjaden@1protocol.com',
    url="https://github.com/1protocol/arbit-native",
    license='GPL3',
    description='Native Arbit client',
    long_description=open('README.md').read(),
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["arbit/arbit_build.py:ffibuilder"],
    install_requires=["cffi>=1.0.0"],
    packages=["arbit"]
)
