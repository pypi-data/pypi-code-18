from datetime import datetime
from pytz import utc


def utcnow():
    "When working with time, assume everything is in UTC"
    return datetime.now(utc)
