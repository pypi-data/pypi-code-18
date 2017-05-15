from __future__ import with_statement
from alembic import context
from sqlalchemy import pool
from logging.config import fileConfig
from results_schema import Base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
import os
import yaml


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

url = os.environ.get('DBURL', None)

if not url:
    db_config_file = context.get_x_argument('db_config_file')\
        .get('db_config_file', None)
    if not db_config_file:
        raise ValueError('No database connection information found')

    with open(db_config_file) as f:
        config = yaml.load(f)
        dbconfig = {
            'host': config['host'],
            'username': config['user'],
            'database': config['db'],
            'password': config['pass'],
            'port': config['port'],
        }
        url = URL('postgres', **dbconfig)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        version_table='results_schema_versions'
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = create_engine(
        url,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table='results_schema_versions'
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
