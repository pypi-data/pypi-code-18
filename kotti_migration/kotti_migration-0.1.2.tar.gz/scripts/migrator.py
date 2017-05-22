import sys
import json
import re
import csv
import uuid
import time
import operator
import random
import transaction
import gzip
import click
import ConfigParser
import subprocess

from pyramid.paster import bootstrap


import sqlalchemy.orm.exc


def get_sql_url(config_file):
    """Returns the sql url from the configuration ini file"""
    config = ConfigParser.ConfigParser()
    config.readfp(open(config_file))
    return config.get('app:kotti', 'sqlalchemy.url', 1)


def get_login_url_db(sql_url=None, config_file=None):
    """ Returns the sql login url and database name from
        the configuration ini file or sql url.
    """
    if not sql_url:
        sql_url = get_sql_url(config_file)
    dbname_index = sql_url.rfind("/")
    dbname = sql_url[dbname_index+1:]
    login_url = sql_url[0:dbname_index]
    if '@' not in sql_url:
        login_url = sql_url
        dbname = sql_url.split('//')[1]
    if "?" in dbname:
        dbname = dbname[:dbname.index("?")]
    return login_url, dbname


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.command()
@click.argument('config_file', type=click.Path('r'))
@click.argument('postgres_url')
@click.option('--login/--no-login', default=True,
              help="Use the SQL URL found in the configuration file to create the new site if --login is used, else use createdb and dropdb to carry out this task.")
@click.option('--yes', is_flag=True, callback=abort_if_false,
              help="Skip the prompt message and proceed with dropping and create a new site",
              expose_value=False,
              prompt='This will erase all pervious data, are you sure you want to create a new site?')
def clone_db(config_file, postgres_url, login, **kwargs):
    """ Drop the current database and clone the given database.

    Executing this command will drop and recreate the database for this application.

    Arguments:

        config_file:     Path to your init file from the current directory

        postgres_url:    URL of the database to clone into the existing database.

    """
    if not postgres_url.startswith("postgres://"):
        print "Invalid postgres url"
    start_time = time.time()
    sql_url = get_sql_url(config_file=config_file)
    login_url, dbname = get_login_url_db(sql_url=sql_url, config_file=config_file)
    print 'using the following database url: {}'.format(login_url)
    if login:
        subprocess.call(["psql", login_url, "-c",
                         "drop database if exists {};".format(dbname)])
        subprocess.call(["psql", login_url, "-c",
                         "create database {};".format(dbname)])
        subprocess.call(
            ["pg_dump {} | psql {}".format(postgres_url, sql_url)],
            shell=True
        )
    else:
        subprocess.call(["dropdb","--if-exists","{}".format(dbname)])
        subprocess.call(["createdb", "{}".format(dbname)])
        subprocess.call(
            ["pg_dump {} | psql {}".format(postgres_url, sql_url)],
            shell=True
        )
    print "{} to build a new site.".format(get_end_time(start_time))


def get_end_time(s_time):
    m, s = divmod(int(time.time() - s_time), 60)
    h, m = divmod(m, 60)
    return "It took %d hr(s) : %02d mins : %02d seconds" % (h, m, s)
