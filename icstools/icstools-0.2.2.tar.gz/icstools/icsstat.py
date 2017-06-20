#!/usr/bin/env python3

import argparse
import datetime
import sys

import icalendar

from .utils import get_hashable_field

"""Display stats about calendar events from of an icalendar file (.ics)

Does not output an icalendar file but stats as text (in seconds).

By default only the total duration of all events (in seconds) is shown. But
other metric can be choosen.
"""

GROUP_BY_MAP = {
    'uid': 'UID',
    'start': 'DTSTART',
    'end': 'DTEND',
    'summary': 'SUMMARY',
    'status': 'STATUS',
    'description': 'DESCRIPTION',
}

def printable_timedelta(td, unit, human_readable):
    if human_readable:
        return str(td)
    else:
        if unit == 'hours':
            return str(td.total_seconds()/3600)
        elif unit == 'seconds':
            return str(td.total_seconds())
        else:
            raise ValueError



def parse_args():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--metric', choices=('total_duration', 'count'), default='total_duration')
    args.add_argument('--human-readable', '-H',
                      action='store_true', default=False,
                      help='display stat in human readable (ignoring unit preference)')
    args.add_argument('--unit', choices=('seconds', 'hours'), default='seconds')
    args.add_argument('--group-by', choices=GROUP_BY_MAP.keys(),
                      help="Shows stats groupped by a certain field instead of global total")
    return args.parse_args()

def icsstat(args):
    in_cal = icalendar.Calendar.from_ical(sys.stdin.read())

    if args.group_by:
        groups = {}
        groupping_fieldname = GROUP_BY_MAP[args.group_by]

        for vevent in in_cal.walk('vevent'):
            groupping_key = get_hashable_field(vevent, groupping_fieldname)

            if not groupping_key in groups:
                groups[groupping_key] = []
            groups[groupping_key].append(vevent)

    else:
        groups = {None: in_cal.walk('vevent')}

    for group_name, group_vevents in groups.items():
        group_duration = datetime.timedelta()

        for vevent in group_vevents:
            start = vevent['DTSTART'].dt
            end = vevent['DTEND'].dt
            duration = end - start
            group_duration += duration

        if args.metric == 'total_duration':
            value = printable_timedelta(group_duration, args.unit, args.human_readable)
        elif args.metric == 'count':
            value = str(len(group_vevents))

        if args.group_by:
            prefix = '{} '.format(group_name)
        else:
            prefix = ''

        print(prefix+value)


def main():
    args = parse_args()
    icsstat(args)

if __name__ == '__main__':
    main()
