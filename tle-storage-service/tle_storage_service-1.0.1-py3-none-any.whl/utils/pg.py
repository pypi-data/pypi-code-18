# -*- coding: utf-8 -*-
import collections
import inspect
from contextlib import suppress

import aiopg
import aiopg.sa
import sqlalchemy as sa
import sqlalchemy.dialects

from ..log import logger

__all__ = (
    'check_sa_column',
    'get_sa_column',
    'listen_pg_notify',
    'send_pg_notify',
    'insert_do_nothing',
    'parse_sa_filter',
    'parse_sa_order',
    'reset_sequence_query',
    'reset_sequences',
)


async def send_pg_notify(conn, channel, msg):
    logger.debug('Send message to pg channel "{}" -> "{}"'.format(channel, msg))
    query = "NOTIFY \"{}\", '{}'".format(channel, msg)
    if isinstance(conn, aiopg.sa.SAConnection):
        await conn.execute(query)
    elif isinstance(conn, aiopg.Connection):
        async with conn.cursor() as cur:
            cur.execute(query)
    else:
        raise ValueError('Argument `conn` must be is instance '
                         '`aiopg.sa.SAConnection` or `aiopg.Connection`')


async def listen_pg_notify(pool, channel, stop_msg='finish', callback=None):
    async with pool.acquire() as conn:
        if isinstance(conn, aiopg.sa.SAConnection):
            conn = conn.connection

        async with conn.cursor() as cur:
            await cur.execute("LISTEN \"{}\"".format(channel))
            while True:
                msg = await conn.notifies.get()

                if msg.payload.strip() == stop_msg:
                    break

                logger.debug('Receive msg from pg channel "%s" <- %s', msg.channel, msg.payload)

                with suppress(Exception):
                    if callable(callback):
                        result = callback(msg)
                        if inspect.isawaitable(result):
                            await result


def reset_sequence_query(table, column):
    if isinstance(table, sa.Table) and isinstance(column, sa.Column):
        return sa.select([
            sa.func.setval(
                sa.func.pg_get_serial_sequence(table.key, column.key),
                sa.select([sa.func.coalesce(sa.func.max(column), 0) + 1]).as_scalar(),
                sa.false()
            )]
        )


async def reset_sequences(conn, table):
    if not isinstance(table, sa.Table):
        return

    for column in table.columns:
        if isinstance(column.autoincrement, bool) and column.autoincrement:
            q = reset_sequence_query(table, column)
            q is not None and await conn.scalar(q)


async def insert_do_nothing(conn, table, values, returning=None):
    """
    This function do insert into table, if row is not already exists.

    :param conn: instance aiopg.sa.SAConnection
    :param values: list with values for insert statement
    :param returning: returning clause for insert statement.
    :return: instance aiopg.sa.ResultProxy
    """

    if not isinstance(table, sa.Table):
        raise ValueError('Argument `table` must be is instance `sqlalchemy.Table`')

    # Reset sequences after insert's conflicts
    await reset_sequences(conn, table)

    insert_stmt = sa.dialects.postgresql.insert(table).values(values)

    if isinstance(returning, collections.Iterable) and not isinstance(returning, str):
        insert_stmt = insert_stmt.returning(*returning)

    # Insert new TLE if already exists do nothing
    return await conn.execute(insert_stmt.on_conflict_do_nothing())


def parse_sa_filter(table, key, value):
    term = get_sa_column(table, key)
    if term is None:
        return []

    comparisons = {
        "$ne": lambda c, v: c.notilike(v),
        "$gt": lambda c, v: c > v,
        "$gte": lambda c, v: c >= v,
        "$lt": lambda c, v: c < v,
        "$lte": lambda c, v: c <= v,
        "$eq": lambda c, v: c == v,
        "$neq": lambda c, v: c != v,
        "$in": lambda c, v: c.in_(v),
        "$nin": lambda c, v: c.notin_(v),
        "$is": lambda c, v: c.is_(v),
        "$contains": lambda c, v: c.contains(v),
        "$like": lambda c, v: c.like(v),
        "$ilike": lambda c, v: c.ilike(v),
        "$startswith": lambda c, v: c.startswith(v),
        "$endswith": lambda c, v: c.endswith(v),
        "$isnot": lambda c, v: c.isnot(v)
    }

    if isinstance(term.type, (sa.dialects.postgresql.JSONB, sa.dialects.postgresql.JSON)):
        return [comparisons.get(o)(term[k].astext, v)
                for k, comprs in value.items()
                for o, v in comprs.items()
                if o in comparisons]
    elif not isinstance(value, dict):
        return [term.ilike("%{}%".format(value)) if isinstance(term.type, (sa.String, sa.Text)) else term == value]

    return [comparisons.get(o)(term, v) for o, v in value.items() if o in comparisons]


def parse_sa_order(table, order):
    result = []
    if isinstance(order, str) and order in table.columns:
        result.append(table.columns.get(order))
    elif isinstance(order, dict):
        for key, value in order.items():
            if check_sa_column(table, key) and value in ('asc', 'desc'):
                term = get_sa_column(table, key)
                result.append(dict(asc=term.asc(), desc=term.desc())[value])
    elif isinstance(order, (set, list, frozenset, tuple)):
        for key in order:
            if check_sa_column(table, key):
                result.append(get_sa_column(table, key))
    return result


def get_sa_column(table, key):
    if not isinstance(table, sa.Table):
        raise ValueError('Argument `table` must be is instance `sqlalchemy.Table`')
    return table.columns.get(key, None)


def check_sa_column(table, key):
    if not isinstance(table, sa.Table):
        raise ValueError('Argument `table` must be is instance `sqlalchemy.Table`')
    return key in table.columns