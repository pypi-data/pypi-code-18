"""Sebureem

Sebureem is a comment server similar to Discuss.
Is purpose is to allow add easily comment sections to web pages.

Sebureem is powered by Bottle for the webserver and use Peewee ORM and SQLite 
for handling data persistence.

"Sebureem" is the Kotava word for "comments" or "group of comments"

"""
import os
import configparser
from flask import Flask
from peewee import SqliteDatabase

__version__ = "0.2.1"

app = Flask(__name__)

config = configparser.ConfigParser()
db = SqliteDatabase(None)
if os.name == "posix":
    config_path = os.path.expandvars('$XDG_CONFIG_HOME/sebureem/sebureem.ini')
elif os.name == "nt":
    config_path = os.path.expandvars('%LOCALAPPDATA%/sebureem/sebureem.ini')

try:
    config.read_file(
        open(config_path)
    )
    db.init(config['DATABASE']['path'])
except (FileNotFoundError, KeyError):
    print("Warning: Sebureem doesn't have config file.")
    print("Please fix it with the `> sebureem --init` command.")

import sebureem.views
