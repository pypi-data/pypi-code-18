import sys
import csv

import termcolor

from .. import consts
from .. import logger

def output_as_csv(stats_tuples, filename):
    if filename is not None:
        with open(filename + '.csv', 'w', newline='') as csv_file:
            _write_as_csv(stats_tuples, csv_file)
    else:
        _write_as_csv(stats_tuples, sys.stdout)

def _write_as_csv(stats_tuples, stream):
    logger.get_logger().info(
        'writes the stats as %s to %s',
        termcolor.colored('CSV', 'green'),
        termcolor.colored(str(stream), 'blue'),
    )

    csv_writer = csv.writer(stream)
    csv_writer.writerow(consts.STATS_TUPLE_ITEMS_NAMES)
    for stats_tuple in stats_tuples:
        csv_writer.writerow(stats_tuple)
