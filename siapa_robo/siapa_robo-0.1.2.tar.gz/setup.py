from setuptools import setup, find_packages
setup(
    name="siapa_robo",
    version="0.1.2",
    author="Rafael Alves Ribeiro",
    author_email="rafael.alves.ribeiro@gmail.com",
    packages=["siapa_robo"],
    install_requires=[
        "brazilnum >= 0.8.8",
        "selenium >= 3.3.1",
        "colorama >= 0.3.9",
        "pandas >= 0.19.2"
    ],
)
