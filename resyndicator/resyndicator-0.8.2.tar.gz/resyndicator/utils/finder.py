import argparse
import sys
import requests
import lxml.html

from functools import wraps
from urllib.parse import urlparse, urlunparse, urljoin
from .logger import logger


def output(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        for line in func(self, *args, **kwargs):
            if self.output is not None:
                self.output.write(line)
                self.output.write('\n')
                self.output.flush()
            yield line
    return wrapper


class Finder:

    common_feed_paths = [
        '/feed/atom/',
        '/?feed=atom',
        '/feed/',
        '/feed',
        '/feeds/posts/default',
        '/atom.xml',
        '/rss.xml',
        '/feed.xml',
        '/feed.rss',
        '/rss/',
        '/.rss',
        '/start.rss',
    ]

    common_feed_xpaths = [
        '//link[@type="application/atom+xml"]/@href',
        '//link[@type="application/rss+xml"]/@href',
    ]

    common_sitemap_paths = [
        '/sitemap.xml',
        '/sitemap.xml.gz',
        '/news-sitemap.xml',
        '/news-sitemap.xml.gz',
    ]

    shibboleths = [
        '<sitemapindex',
        '<urlset',
        '<feed',
        '<rss',
    ]

    def __init__(self, url, output=None):
        self.url = urlunparse(urlparse(url)[:2] + ('',)*4)
        self.output = output
        self.session = requests.session()

    def _request(self, url, head=False, **kwargs):
        logger.info('%s %r', 'Testing' if head else 'Retrieving', url)
        request = self.session.head if head else self.session.get
        try:
            response = request(url, timeout=5, verify=False, allow_redirects=True, **kwargs)
        except (IOError, requests.RequestException) as excp:
            logger.error('Request exception %r for %s', excp, self.url)
        else:
            return response

    def _try_paths(self, paths):
        for path in paths:
            url = self.url + path
            response = self._request(url)
            if response and response.status_code in range(200, 300):
                if any(shibboleth in response.text for shibboleth in self.shibboleths):
                    return response.url
            elif not response:  # Connection error
                return

    @output
    def feeds(self):
        count = 0
        response = self._request(self.url)
        if response and response.status_code in range(200, 400):
            root = lxml.html.fromstring(response.content)
            for xpath in self.common_feed_xpaths:
                for link in root.xpath(xpath):
                    yield urljoin(self.url, link)
                    count += 1
        if not count:
            link = self._try_paths(self.common_feed_paths)
            if link:
                yield link
                count += 1
        if not count:
            logger.warn('No feeds for %r', self.url)

    @output
    def sitemaps(self):
        count = 0
        robots_url = self.url + '/robots.txt'
        response = self._request(robots_url)
        if response and response.status_code in range(200, 400):
            for line in response.text:
                line = line.strip()
                if line.startswith('Sitemap:'):
                    link = line[len('Sitemap:'):].strip()  # Usually space after colon
                    yield urljoin(self.url, link)
                    count += 1
        if not count:
            link = self._try_paths(self.common_sitemap_paths)
            if link:
                yield link
                count += 1
        if not count:
            logger.warn('No sitemaps for %r', self.url)


def run():
    parser = argparse.ArgumentParser(description='Find feeds and sitemaps.')
    parser.add_argument('input', help='The input file – one site per line')
    args = parser.parse_args(sys.argv[1:])
    with open(args.input) as inputfile:
        for line in inputfile.readlines():
            line = line.strip()
            if not line:
                continue
            finder = Finder(line, output=sys.stdout)
            list(finder.feeds())
            list(finder.sitemaps())
