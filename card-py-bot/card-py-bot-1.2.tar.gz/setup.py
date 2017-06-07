from setuptools import setup, find_packages


setup(
    name="card-py-bot",
    author="Nathan Klapstein",
    author_email="nklapste@ualberta.ca",
    version="1.2",
    description="A Discord Bot for parsing magic card links",
    url="https://github.com/nklapste/card-py-bot",
    download_url="https://github.com/nklapste/card-py-bot/archive/1.2.tar.gz",
    packages=["card_py_bot"],
    package_data={
        '': ['README.md'],
        'card_py_bot': ['mana_config.txt', 'MANA_ICONS/*.gif'],
    },
    install_requires=[
        'beautifulsoup4',
        'discord.py',
    ],
    entry_points={
        'console_scripts': ['card-py-bot = card_py_bot.py_d_bot:main'],
    },
)
