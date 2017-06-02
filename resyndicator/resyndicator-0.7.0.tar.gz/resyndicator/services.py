import importlib
import requests
import argparse
from itertools import cycle
from time import sleep, time
from xml.sax import SAXException
from xml.etree.ElementTree import ParseError
from . import settings
from .utils.logger import logger
from .utils.sitemapparser import SitemapParsingException
from .fetchers.base import UnchangedException

resources = importlib.import_module(settings.RESOURCES)


def fetchers(args):
    """Main entry point to the fetchers, which run periodically."""
    parser = argparse.ArgumentParser(description='Run all fetchers via a scheduler.')
    parser.add_argument('--test-mode', dest='testmode', action='store_true')
    args = parser.parse_args(args)
    while True:
        cycle_start = time()
        pending_feeds = list(feed for feed in resources.FETCHERS
                             if feed.needs_update)
        if args.testmode and not pending_feeds:
            logger.info('Running in test mode')
            pending_feeds += resources.FETCHERS
        fresh_entries = []  # For PubSubHubbub
        for feed in pending_feeds:
            logger.info('Updating %s (%.2f seconds behind schedule)',
                        feed, time() - feed.next_check)
            try:
                feed.update()
            except (IOError, requests.RequestException) as excp:
                logger.error('Request exception %r for %s',
                             excp, feed.url)
            except (SAXException, ParseError, SitemapParsingException) as excp:
                logger.error('Parser exception %r for %s',
                             excp, feed.url)
            except UnchangedException:
                logger.info('Source unchanged')
            else:
                entries = feed.persist()
                fresh_entries.extend(entries)
            feed.clean()
            feed.touch()
        logger.info('Updating resyndicators')
        for resyndicator in resources.RESYNDICATORS:
            resyndicator.publish()
            resyndicator.pubsub(fresh_entries)
        sleep_time = cycle_start + settings.FETCHER_SLEEP - time()
        if sleep_time > 0:
            logger.debug('Sleeping %.2f s', sleep_time)
            sleep(sleep_time)


def content(args):
    """Main entry point to the content fetchers."""
    parser = argparse.ArgumentParser(description='Run a daemon that retrieves content.')
    args = parser.parse_args(args)
    fetchers = resources.CONTENT_FETCHERS
    for fetcher in cycle(fetchers):
        fetcher.fetch()
        fetcher.persist()
        sleep(settings.CONTENT_FETCHER_SLEEP)


def stream(args):
    """Main entry point to the streams, which run continuously."""
    parser = argparse.ArgumentParser(description='Run a daemon that listens to a stream.')
    parser.add_argument('name', help='Stream name')
    args = parser.parse_args(args)
    for entries in stream.run():
        for resyndicator in resources.RESYNDICATORS:
            resyndicator.maybe_publish(entries)
