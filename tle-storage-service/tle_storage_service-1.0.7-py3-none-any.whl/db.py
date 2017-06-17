# -*- coding: utf-8 -*-
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.dialects

from .utils import insert_do_nothing, PROJECT_DIR

__all__ = (
    'TLE',
    'insert_tle',
    'metadata',
    'run_migrations',
)

DSN_TPL = 'postgresql+psycopg2://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s'


metadata = sa.MetaData(schema='tle_storage_service')


TLE = sa.Table('tle', metadata,
               sa.Column('id',
                         sa.Integer,
                         primary_key=True,
                         autoincrement=True),
               sa.Column('norad_cat_id',
                         sa.Integer,
                         nullable=False),
               sa.Column('dt',
                         sa.DateTime,
                         nullable=False),
               sa.Column('tle_line1',
                         sa.String(69),
                         nullable=False),
               sa.Column('tle_line2',
                         sa.String(69),
                         nullable=False),
               sa.Column('extra_info',
                         sa.dialects.postgresql.JSONB(none_as_null=True)),
               sa.Column('source',
                         sa.Enum('space-track', 'nasa', name='tle_source_enum', schema=metadata.schema),
                         nullable=False,
                         default='space-track',
                         server_default='space-track'),
               sa.Column('created_at',
                         sa.DateTime,
                         nullable=False,
                         default=datetime.utcnow(),
                         server_default=sa.text("(now() at time zone 'utc')")),
               sa.Column('updated_at',
                         sa.DateTime,
                         nullable=False,
                         default=datetime.utcnow(),
                         onupdate=datetime.utcnow(),
                         server_onupdate=sa.text("(now() at time zone 'utc')"),
                         server_default=sa.text("(now() at time zone 'utc')")),
               sa.Column('is_deleted',
                         sa.Boolean,
                         default=False,
                         server_default=sa.false(),
                         nullable=False),
               sa.UniqueConstraint('norad_cat_id', 'dt', 'source', 'is_deleted'))


def run_migrations(db_params):
    import os
    from alembic import command, config

    os.chdir(PROJECT_DIR)

    db_params.setdefault('host', 'localhost')
    db_params.setdefault('port', 5432)

    alembic_cfg = config.Config(os.path.join(PROJECT_DIR, 'alembic.ini'))
    alembic_cfg.set_main_option('sqlalchemy.url', DSN_TPL % db_params)
    alembic_cfg.attributes['configure_logger'] = False

    command.upgrade(alembic_cfg, 'head')


async def insert_tle(conn, values, returning=False):
    """
    This function do insert into `TLE` table, if row is not already exists.

    :param conn: Instance aiopg.sa.SAConnection
    :param values: List with values for insert statement
    :param returning: Flag for enable returning inserted row.
                      Pass `False` for disable returning,
                      by default returning is id
    :return: Instance aiopg.sa.ResultProxy
    """
    if returning:
        returning = TLE
    return await insert_do_nothing(conn, TLE, values, returning)
