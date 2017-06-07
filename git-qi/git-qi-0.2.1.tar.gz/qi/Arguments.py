"""Exports 'A', which holds parsed CLI arguments."""

from dateutil.relativedelta import relativedelta as td
from qi import TimeIterators as T
from qi import GitClient as git
from datetime import datetime
import argparse
import time
import os
import re

timeunits=['hour', 'day', 'week', 'month', 'year']

# Enforces format of the --past/-p option
def relative_user_epoch(s):
    if re.search('^\d+ ({})s?$'.format('|'.join(timeunits)), s) is None:
        msg = (
                "You must specify a format like '3 months' or '1 year' "
                " using one of these units: {}".format(', '.join(timeunits))
        )
        raise argparse.ArgumentTypeError(msg)
    return s

class constrained_epoch(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):

                # Convert '3 months' to ('3', ' ', 'months')
                split = values.partition(' ')

                # Normalize inclusion of 's'. i.e. "month" -> "months"
                unit_as_written = split[2]
                if unit_as_written[-1] != 's':
                    unit_as_written = unit_as_written + 's'

                # Compute accurate time delta from human expression.
                # If argument is "3 months", dict looks like:
                # {hours: 0, days: 0, weeks: 0, months: 3, years: 0}
                units = {k + 's': int(split[0]) * int(k + 's' == unit_as_written) for k in timeunits}

                # The beginning of Git commit history that the user deems important.
                user_epoch = datetime.utcfromtimestamp(git.headtime()) - td(**units)

                # We cannot go before the beginning of the commit history.
                timestamp = max(time.mktime(user_epoch.timetuple()), git.inittime())

                setattr(namespace, self.dest, timestamp)

class positive_int(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
                if values <= 0:
                    raise argparse.ArgumentTypeError("positive_int:{0} is not a positive integer".format(values))

                setattr(namespace, self.dest, values)

class select_time_iterator(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):

                generators = {
                        'month': T.months,
                        'week': T.weeks,
                        'day': T.days,
                        'hour': T.hours,
                        'year': T.years,
                }

                setattr(namespace, self.dest, generators.get(values, T.weeks))

parser = argparse.ArgumentParser(description="Prints commits at the end of time intervals.", fromfile_prefix_chars="@")
parser.add_argument("-e", "--every", type=str, default='week', action=select_time_iterator, choices=timeunits, help="Length of time between revisions.")
parser.add_argument("-p", "--past", required=True, type=relative_user_epoch, action=constrained_epoch, help="How long ago to consider commits relevant. i.e. '3 months' or '1 year'.")
parser.add_argument("-c", "--command", type=str, help="Check out each found commit and run command. Unclean termination of Qi will leave HEAD detached.")
parser.add_argument("-d", "--dates", action='store_true', default=False, help="Print committer dates alongside commits. Ignored if -c is specified.")

A = parser.parse_args()
