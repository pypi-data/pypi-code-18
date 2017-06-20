#!/usr/bin/env python3

import argparse
import sys

import icalendar

from .utils import get_hashable_field

"""uniq-like on icalendar files (.ics) : remove duplicate events

By default, remove duplicates according to UID, but duplication could do the
match on other criterions.

When removing duplicates, only the first duplicate is kept.
"""

UNIQUE_ON_ARG_MAP = {
    'uid': 'UID',
    'start': 'DTSTART',
    'end': 'DTEND',
    'summary': 'SUMMARY',
    'status': 'STATUS',
    'description': 'DESCRIPTION',
}

def parse_args():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument(
        '--unique-on', nargs='+', default=['uid'],
        choices=UNIQUE_ON_ARG_MAP.keys(),
        help='keys for deduplication (they are and-combined)')
    args.add_argument(
        '--add-prefix', default='',
        help="Mark deduplicated entries with a prefix on their summary"
    )
    args.add_argument(
        '--verbose', '-v', action='store_true', default=False,
        help="Display metrics informations on stderr"
    )
    return args.parse_args()


def uniq(args):
    in_cal = icalendar.Calendar.from_ical(sys.stdin.read())

    existing_events = set()

    key_fields = [UNIQUE_ON_ARG_MAP[i] for i in args.unique_on]

    def get_key(vevent):
        return tuple(get_hashable_field(vevent, field) for field in key_fields)


    kept_events = []
    duplicate_events = set()
    for vevent in in_cal.walk('vevent'):
        key = get_key(vevent)
        if not key in existing_events:
            existing_events.add(key)
            kept_events.append(vevent)
        else:
            duplicate_events.add(key)
            if args.verbose:
                sys.stderr.write(
                    'Duplicate item: {}({})\n'.format(
                        vevent['SUMMARY'], vevent['UID']))

    out_cal = icalendar.Calendar()
    for vevent in kept_events:
        if get_key(vevent) in duplicate_events:
            vevent['SUMMARY'] = '{}{}'.format(args.add_prefix, vevent['SUMMARY'])
        out_cal.add_component(vevent)

    sys.stdout.write(out_cal.to_ical().decode('utf-8'))

def main():
    args = parse_args()
    uniq(args)

if __name__ == '__main__':
    main()
