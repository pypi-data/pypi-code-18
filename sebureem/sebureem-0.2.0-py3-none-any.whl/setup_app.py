"""Sebureem Setup webinstaller

This specific webapp is designed to fire a webserver allowing the Sebureem
administrator to setup its instance.

The command to start the webapp is ``> sebureem --init``. Webapp is served
at ``localhost`` on port ``8080``. 
"""
import os
import bcrypt
from pathlib import Path
from configparser import ConfigParser
from flask import Blueprint, render_template, flash, request
from peewee import SqliteDatabase, OperationalError

from sebureem import db, config
from sebureem.models import Sebura, Sebuks

__all__ = ["setup_app"]

setup_app = Blueprint("setup", __name__,
        url_prefix="/install", template_folder="templates")

def config_dir():
    """Return the config path depending on the server OS
    """
    if os.name == "posix":
        config_path = Path(
            os.path.expandvars('$XDG_CONFIG_HOME/sebureem')
        )
    elif os.name == "nt":
        config_path = Path(
            os.path.expandvars('%LOCALAPPDATA%/sebureem')
        )
    return config_path

@setup_app.route('/')
def index():
    """Simply return the startpage of the setup webapp
    """
    return render_template("setup/index.html")

@setup_app.route('/config/')
def create_config():
    """Create the Sebureem server config file
    """
    try:
        config_path = config_dir()
        config_path.mkdir(mode=0o755, parents=True, exist_ok=True)
        config_file = config_path / 'sebureem.ini'
        if config_file.exists():
            raise FileExistsError
        print(str(config_file))
        with open(str(config_file), "w") as f:
            f.write("# Sebureem config file")
        flash("Success: Config file created", "success")
    except FileExistsError:
        flash("Warning: Config file found", "error")
        return render_template("setup/config.html",
            config_path=config_path / 'sebureem.ini',
            override_form=True)

    return render_template("setup/config.html",
        config_path=config_file, override_form=False)

@setup_app.route('/database/', methods=['GET', 'POST'])
def create_db():
    """Allow user to set up database

    Allow user select path for the Sebureem SQLite database then create it.
    A flash message confirm a successful creation.
    """
    if request.method == 'GET':
        if os.name == "posix":
            db_default_path = os.path.expandvars('$XDG_DATA_HOME/sebureem')
        elif os.name == "nt":
            db_default_path = os.path.expandvars('%LOCALAPPDATA%\sebureem')
        return render_template("setup/database.html",
            database_path=db_default_path,
            created=False)

    if request.method == 'POST':
        db_path = Path(request.form['db_path'])
        db_path = db_path / request.form['db_name']

        try:
            db.init(str(db_path))
            db.connect()
            db.create_tables([Sebura, Sebuks])
            db.close()
            flash("Success: Database created", "success")
        except OperationalError:
            flash("Warning: Database already present at this location", "error")

        config['DATABASE'] = { 
            'path': db_path
        }
        config_path = config_dir()
        config_file = config_path / 'sebureem.ini'
        with open(str(config_file), 'w') as conf:
            config.write(conf)
        return render_template("setup/database.html",
            database_path=str(db_path),
            created=True)

@setup_app.route('/admin/', methods=['GET', 'POST'])
def create_admin():
    """Allow user to set up admin credentials

    Allow the user to set up credentials to access the Sebureem Admin Webpanel.
    Login is written in plain text, but password is hashed using bcrypt
    algorythm.
    """
    if request.method == 'GET':
        return render_template("setup/admin.html",
            created=False)

    if request.method == 'POST':
        admin_login = request.form['admin_login']
        admin_passwd = bcrypt.hashpw(
            bytes(request.form['admin_passwd'], 'utf-8'), 
            bcrypt.gensalt()
        )
        config['ADMIN'] = {
            'login': admin_login,
            'passwd': admin_passwd.decode('utf-8')
        }
        config_path = config_dir()
        config_file = config_path / 'sebureem.ini'
        with open(str(config_file), 'w') as conf:
            config.write(conf)
        flash("Success: Admin account created", "success")
        return render_template("setup/admin.html",
            created=True)

@setup_app.route('/site/', methods=['GET', 'POST'])
def create_site():
    """Allow user to set up a fist site for Sebureem

    Create a first site for Sebureem to accept comment from.
    """
    if request.method == 'GET':
        return render_template("setup/site.html")

    if request.method == 'POST':
        site_name = request.form['site_name'] 
        site_url = request.form['site_url']
        config[site_name] = {
            'url': site_url
        }
        config_path = config_dir()
        config_file = config_path / 'sebureem.ini'
        with open(str(config_file), 'w') as conf:
            config.write(conf)
        flash("Success: Site configured")
        return render_template("setup/site.html",
            created=True)
