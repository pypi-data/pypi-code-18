#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Get a Human string ISO-8601 representation of datetime.datetime with UTC.
Other solutions I found on the internet needs importing 'time' this one dont.
ISO-8601 standard:Its permitted to omit the 'T' character by mutual agreement.
"""


import datetime


def get_human_datetime(date_time=None):
    """Get a Human string representation of datetime with UTC info."""
    if date_time and isinstance(date_time, datetime.datetime):  # arg datetime
        return date_time.replace(microsecond=0).astimezone().isoformat(" ")
    else:  # now datetime
        return datetime.datetime.now(datetime.timezone.utc).replace(
            microsecond=0).astimezone().isoformat(" ")
