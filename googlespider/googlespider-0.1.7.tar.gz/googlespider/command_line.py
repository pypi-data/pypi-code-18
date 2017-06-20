#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Main entry point for command line Google
search client.
"""
import argparse
import csv
import json
import logging
import sys
import time

from .spider import GoogleSpider


def _get_args():
    """
    Parse command line arguments.
    """
    description = """
    Command line Google search.
    """
    argparser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@',
        add_help=True)

    argparser.add_argument('queries',
                           nargs='*',
                           default=[],
                           help=('google search queries (use @filename to read from file)'))

    argparser.add_argument('-v',
                           '--verbose',
                           action='count',
                           dest='level',
                           default=2,
                           help='verbose logging (repeat for more verbose)')

    argparser.add_argument('-c',
                           '--country',
                           dest='country',
                           type=str,
                           default='us',
                           help=('google search country as ISO-3166 country code (e.g. uk, us, ca)'))

    argparser.add_argument('-p',
                           '--proxy',
                           dest='proxy',
                           help=('proxy string '
                                 '(protocol://username:password@ip:port)'))

    argparser.add_argument('-l',
                           '--language',
                           dest='language',
                           type=str,
                           default='en-US',
                           help=('ACCEPT-LANGUAGE request header (e.g. en-us, en-gb, en) '
                                 '(More examples: '
                                 'https://msdn.microsoft.com/en-gb/library/'
                                 'ee825488(v=cs.20).aspx)'))

    argparser.add_argument('-L',
                           '--localise',
                           dest='localise',
                           action="store_true",
                           help=('localise language to country '
                                 '(overrides -l)'))

    argparser.add_argument('-n',
                           '--num-results',
                           dest='num_results',
                           type=int,
                           default=10,
                           help=('number of results to fetch (1 - 1000)'))

    argparser.add_argument('-d',
                           '--delay',
                           dest='delay',
                           type=int,
                           default=30,
                           help=('seconds to wait between requests'))

    argparser.add_argument('-i',
                           '--ignore-https',
                           dest='ignore',
                           action="store_true",
                           help=('supress HTTPS warnings'))

    argparser.add_argument('-r',
                           '--results-per-page',
                           dest='results_per_page',
                           type=int,
                           default=100,
                           help=('number of results per page (1 - 100)'))

    argparser.add_argument('-s',
                           '--start-index',
                           dest='start_index',
                           type=int,
                           default=0,
                           help=('start index (1 - 999)'))

    argparser.add_argument('-f',
                           '--format',
                           dest='output_format',
                           type=str,
                           choices=['json', 'tsv', 'csv'],
                           default='tsv',
                           help='output format')

    argparser.add_argument('--min-date',
                           type=str,
                           help=('minimum date, US format, dd/mm/yyyy '))

    argparser.add_argument('--max-date',
                           type=str,
                           help=('max date, US format, dd/mm/yyyy '))

    args = argparser.parse_args()

    # Validate
    if not args.queries:
        argparser.error('No search queries provided.')

    return args


def _print_data(data, output_format='tsv'):
    """
    Print data in specified format.
    """
    if output_format == 'tsv':
        writer = csv.writer(sys.stdout, delimiter='\t')  # stdout file doesn't require open()/close()
        writer.writerow(data)
    elif output_format == 'csv':
        writer = csv.writer(sys.stdout)  # stdout file doesn't require open()/close()
        writer.writerow(data)
    elif output_format == 'json':
        print(json.dumps(data))
    else:
        raise ValueError('Unsupported format (tsv, csv, json)')


def main():
    log_format = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]

    args = _get_args()

    logging.basicConfig(
        level=levels[min(args.level, len(levels) - 1)],
        format=log_format
    )

    count = 0
    for query in args.queries:
        spider = GoogleSpider(query=query,
                              country=args.country,
                              language=args.language,
                              results_per_page=args.results_per_page,
                              max_results=args.num_results,
                              proxy=args.proxy,
                              wait_time=args.delay,
                              ignore_https_warnings=args.ignore,
                              start=args.start_index,
                              min_date=args.min_date,
                              max_date=args.max_date,
                              localise=args.localise)

        results = spider.crawl()
        rank = 1

        for result in results:
            data = [query, rank, result[0]]
            _print_data(data, args.output_format)
            rank += 1

        count += 1
        if count < len(args.queries):
            time.sleep(spider.wait_time)
