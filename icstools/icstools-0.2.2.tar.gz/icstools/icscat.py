#!/usr/bin/env python3

import argparse
import sys

import icalendar

"""cat-like on icalendar files (.ics)

Concatenate two or more ics files to the standard output
There is only one vcalendar in the output.
"""

def parse_args():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument(
        'input_files', nargs='+',
        help='The file(s) to concatenate to standard output')

    return args.parse_args()


def cat(args):
    out_cal = icalendar.Calendar()

    for ics_path in args.input_files:
        in_cal = icalendar.Calendar.from_ical(open(ics_path).read())
        for vevent in in_cal.walk('vevent'):
            out_cal.add_component(vevent)

    sys.stdout.write(out_cal.to_ical().decode('utf-8'))


def main():
    args = parse_args()
    cat(args)


if __name__ == '__main__':
    main()
