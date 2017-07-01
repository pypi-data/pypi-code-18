import argparse
import datetime

import tzlocal
import parsedatetime
import pytimeparse

from . import consts

class HelpFormatter(
    argparse.RawTextHelpFormatter,
    argparse.ArgumentDefaultsHelpFormatter,
):
    pass

_SEARCH_FIELDS = ['name', 'description']
_LOCAL_TIME_ZONE = tzlocal.get_localzone()

def parse_options():
    parser = argparse.ArgumentParser(
        prog=__package__.replace('_', '-'),
        formatter_class=HelpFormatter,
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        help='show the version message and exit',
        version='{:s}, v{:s}\n'.format(consts.APP_NAME, consts.APP_VERSION) \
            + 'Copyright (C) 2017 thewizardplusplus',
    )
    parser.add_argument(
        '-a',
        '--areas',
        nargs='+',
        default=['1'],
        help='vacancies areas',
    )
    parser.add_argument(
        '-s',
        '--specializations',
        nargs='+',
        default=['1.221'],
        help='vacancies specializations',
    )
    parser.add_argument(
        '-q',
        '--query',
        default='',
        help='the additional search query',
    )
    parser.add_argument(
        '-p',
        '--query-properties',
        choices=_SEARCH_FIELDS,
        nargs='+',
        default=_SEARCH_FIELDS,
        help='search fields for the search query',
    )
    parser.add_argument(
        '-r',
        '--salary-required',
        action='store_true',
        help='search vacancies only with a salary',
    )
    parser.add_argument(
        '-b',
        '--analysis-begin',
        type=_parse_timestamp,
        default='1 month ago',
        help='a begin of the analysis time period ' \
            + 'in the ISO 8601 or the human-readable format',
    )
    parser.add_argument(
        '-e',
        '--analysis-end',
        type=_parse_timestamp,
        default='now',
        help='an end of the analysis time period ' \
            + 'in the ISO 8601 or the human-readable format',
    )
    parser.add_argument(
        '-I',
        '--analysis-increment',
        type=_parse_time_delta,
        help='the analysis time increment in the human-readable format',
    )
    parser.add_argument(
        '-F',
        '--request-frequency',
        type=float,
        default=30,
        help='the maximal request frequency',
    )
    parser.add_argument(
        '-S',
        '--page-size',
        type=int,
        default=500,
        help='the maximal page size',
    )
    parser.add_argument(
        '-V',
        '--value-of-interest',
        type=int,
        default=5,
        help='the minimal value of an interest',
    )
    parser.add_argument(
        '-E',
        '--error-on-limit',
        action='store_true',
        help='throw an error on an exceeding of the search limit',
    )
    parser.add_argument(
        '-D',
        '--skills-delimiters',
        nargs='*',
        default=[',', ';'],
        help='delimiters for unseparated skills',
    )
    parser.add_argument(
        '-A',
        '--skills-aliases',
        help='the path to a file with skills aliases in a JSON format',
    )
    parser.add_argument(
        '-O',
        '--order',
        choices=consts.STATS_TUPLE_ITEMS_MAP.keys(),
        default='num',
        help='the order of stats items',
    )
    parser.add_argument(
        '-f',
        '--format',
        choices=['raw', 'csv', 'svg'],
        nargs='+',
        default=['svg'],
        help='the output format',
    )
    parser.add_argument('-i', '--inputs', nargs='+', help='input paths')
    parser.add_argument('-o', '--output', help='the output path')

    return parser.parse_args()

def _parse_timestamp(value):
    timestamp = None
    try:
        timestamp = datetime.datetime.strptime(value, consts.TIMESTAMP_FORMAT) \
            .astimezone(_LOCAL_TIME_ZONE)
    except Exception:
        timestamp, status = parsedatetime.Calendar().parseDT(value)
        if status == 0:
            raise argparse.ArgumentTypeError(
                'timestamp {:s} is incorrect'.format(value),
            )

        timestamp = _LOCAL_TIME_ZONE.localize(timestamp, is_dst=None)

    return timestamp

def _parse_time_delta(value):
    if value is None:
        return None

    seconds = pytimeparse.parse(value)
    if seconds is None:
        raise argparse.ArgumentTypeError(
            'time delta {:s} is incorrect'.format(value),
        )

    return datetime.timedelta(seconds=seconds)
