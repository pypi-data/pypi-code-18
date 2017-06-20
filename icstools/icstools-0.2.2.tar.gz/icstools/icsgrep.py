#!/usr/bin/env python3

import argparse
import sys

import icalendar

"""grep-like on calendar events from an icalendar file (.ics)

Filters calendar events on summary field, in order to include/exclude VEVENTS
from output.

Option names are very similar to grep options.
"""

def parse_args():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument(
        'pattern',
        help='Retain only the vevents having this pattern in their summary')
    args.add_argument(
        '--invert-match', '-v', default=False, action='store_true',
        help='The inclusion pattern becomes an exclusion pattern')
    args.add_argument(
        '--ignore-case', '-i', default=False, action='store_true',
        help='Case-insensitive pattern')

    return args.parse_args()


def _match(needle, hay, invert=False, ignore_case=False):
    if ignore_case:
        needle, hay = needle.lower(), hay.lower()

    has_match = needle in hay
    if invert:
        return not has_match
    else:
        return has_match


def grep(args):
    pattern = args.pattern

    in_cal = icalendar.Calendar.from_ical(sys.stdin.read())
    out_cal = icalendar.Calendar()

    for vevent in in_cal.walk('vevent'):
        if _match(pattern, vevent['SUMMARY'], args.invert_match, args.ignore_case):
            out_cal.add_component(vevent)

    sys.stdout.write(out_cal.to_ical().decode('utf-8'))

def main():
    args = parse_args()
    grep(args)

if __name__ == '__main__':
    main()
