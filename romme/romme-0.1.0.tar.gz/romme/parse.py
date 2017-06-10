# -*- coding: UTF-8 -*-

import re

from romme import names
from romme.romans import roman_to_decimal

# Matches variants of "1[er] fructidor [an ]iii"
RE_STANDARD_DATE = re.compile(r"^(\d+)(?:er)? ([a-z]+?) (?:an )?([xvi]+)$")

# Matches variants of "jour {de la vertue,du genie,...} [an ]iii"
RE_SANSCULOTTIDE_DATE = re.compile(
        r"^(?:jour|sans[ -]?cullotide) (d[a-z ]+?) (?:an )?([xvi]+)$")

def _read_standard_date(match):
    """
    Read a date from a match object that was returned by
    ``RE_REPUBLICAN_DATE.match(...)``. It returns ``None`` if the date can't be
    parsed.
    """
    day_string = match.group(1)

    if not day_string.isnumeric():
        return

    d = int(day_string)

    month_string = match.group(2)
    m = None

    for n, candidate in enumerate(names.months):
        if candidate.sanitized == month_string:
            m = n
            break
    else:
        return

    y = roman_to_decimal(match.group(3))

    return (y, m, d)

def _read_sansculottide_date(match):
    """
    Read a date from a match object that was returned by
    ``RE_SANSCULOTTIDE_DATE.match(...)``. It returns ``None`` if the date can't
    be parsed.
    """
    day_string = match.group(1)
    d = None

    for n, candidate in enumerate(names.sans_culottides):
        if candidate.sanitized == day_string:
            d = n
            break
    else:
        return

    y = roman_to_decimal(match.group(2))

    return (y, 13, d)

def parse_date(s):
    s = names.sanitize_name(s)
    m = RE_STANDARD_DATE.match(s)
    if m:
        return _read_standard_date(m)

    m = RE_SANSCULOTTIDE_DATE.match(s)
    if m:
        return _read_sansculottide_date(m)
