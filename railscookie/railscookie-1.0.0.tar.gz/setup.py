from setuptools import setup

setup(
    name="railscookie",
    version="1.0.0",
    author="orisano",
    author_email="owan.oriasno@gmail.com",
    description="Rails4 Cookie Manipulator for Python3",
    license="MIT",
    url="https://github.com/orisano/railscookiepy",
    py_modules=["railscookie"],
    install_requires=["PyCrypto"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
