"""Sebureem Command Line Utilities

Usage:
    sebureem --init
    sebureem serve [--debug] [<host>] [<port>]
    sebureem admin (-l | -a | -p) <item>

General options:
    --debug         Start the bottle app in debug mode.
    --init          Initialize database.
    -h, --help       Show this screen.
    --version       Show version.

Admin options:
    -l, --lock          Lock specified topic, 
                        <item> must be a topic name or id.
    -u, --unlock        Unlock specified topic, 
                        <item> must be a topic name or id.
    -a, --add-site      Add a new site interactively,
                        <item> must be the site name.
    -r, --remove-site   Remove a site interactively,
                        <item> must be the site name or id.
    -p, --publish       Choose submitted comments to publish, 
                        <item> must be a topic name or id.
"""
import os
from docopt import docopt
from flask import Flask

from sebureem import app, db, config
from sebureem.models import Sebura, Sebuks
from sebureem.setup_app import setup_app


def sebureem():
    args = docopt(__doc__, version='0.0.1')

    if args['--init']:
        init_sebureem()
    elif args['serve']:
        serve(
            args['<host>'] or "localhost",
            args['<port>'] or "8080",
            args['--debug']
        )
    elif args['admin']:
        if args['-l']:
            print("Locking topic ".format(args['<item>']))
        elif args['-a']:
            print("Adding site ".format(args['<item>']))
        elif args['-r']:
            print("Removing site".format(args['<item>']))
        elif args['-p']:
            print("Publishing comments".format(args['<item>']))


def init_sebureem():
    """Serve the Sebureem setup webinstaller

    Installer runs on
    http://localhost:8080/install
    """
    app = Flask(__name__)
    app.register_blueprint(setup_app)
    app.secret_key = "sebureem_setup_secret"
    app.run('localhost', 8080, debug=True)


def serve(host='localhost', port=8080, debug=False):
    if debug:
        app.run(host, int(port), debug=True)
    else:
        app.run(host, int(port))
