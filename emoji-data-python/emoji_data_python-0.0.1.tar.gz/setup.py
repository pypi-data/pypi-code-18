import os

import setuptools

module_path = os.path.join(os.path.dirname(__file__), 'emoji_data_python.py')

setuptools.setup(
    name="emoji_data_python",
    version="0.0.1",
    url="https://gitlab.illuin.tech/bot-factory/emoji_data_python/",

    author="Illuin Technology",
    author_email="contact@illuin.tech",

    description="Python emoji toolkit",
    long_description=open('README.md').read(),

    zip_safe=False,
    platforms='any',

    install_requires=[''],
    packages=setuptools.find_packages(),
    include_package_data=True,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
