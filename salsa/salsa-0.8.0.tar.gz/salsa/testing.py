from collections import namedtuple
from datetime import datetime

from mock import patch
from sqlalchemy import event
import pytz

from .salsa import Session
from .salsa import engine
from . import time


def dbsession(request):
    connection = engine.connect()
    transaction = connection.begin()
    dbsession = Session(bind=connection)
    dbsession.begin_nested()

    @event.listens_for(dbsession, 'after_transaction_end')
    def restart_savepoint(sess, trans):
        if trans.nested and not trans._parent.nested:
            sess.expire_all()
            sess.begin_nested()

    def rollback():
        transaction.rollback()
        dbsession.rollback()
        dbsession.close()
        connection.close()

    request.addfinalizer(rollback)
    return dbsession


def morning():
    now = datetime.now()
    zone = pytz.timezone('America/Los_Angeles')
    dt = zone.localize(datetime(now.year, now.month, now.day, 5))
    return dt


def evening():
    now = datetime.now()
    zone = pytz.timezone('America/Los_Angeles')
    dt = zone.localize(datetime(now.year, now.month, now.day, 19))
    return dt


def py3k_now(request):
    now = lambda: datetime(2008, 12, 3, 12, tzinfo=pytz.utc)
    patcher = patch.object(time, 'utcnow', now)
    cleanup = lambda: patcher.stop()
    request.addfinalizer(cleanup)
    patcher.start()
    return now


_Password = namedtuple("Password", "plaintext salt hash")


def password(request):
    pw = _Password(
        plaintext='dragon',
        salt='$2a$12$WZ5gEu36V57GrVdHBugNie',
        hash='$2a$12$WZ5gEu36V57GrVdHBugNielRoOpS7ncFy5W7N6ZnkWoiKz7QeJ/Ay'
    )
    return pw
