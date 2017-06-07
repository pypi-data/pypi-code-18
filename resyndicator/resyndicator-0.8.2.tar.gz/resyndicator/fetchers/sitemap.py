import json
import requests
import dateutil.parser
from datetime import datetime
from utilofies.stdlib import canonicalized
from ..utils import urn_from_string, stopwatch, process_time
from ..utils.logger import logger
from ..utils.sitemapparser import SitemapIndex, Sitemap
from .base import BaseEntryInterface, BaseFetcher, UnchangedException
from .. import settings


class SitemapEntryInterface(BaseEntryInterface):
    """
    Entry mapping for the sitemap entry.
    """

    @property
    def source(self):
        """Entry raw source as JSON inside an HTML snippet."""
        return ('<details>\n'
                '<summary>JSON Source</summary>\n'
                '<div class="entry-source">{}</div>\n'
                '</details>').format(json.dumps(
                    self.raw_entry, indent=4, sort_keys=True, default=str))

    @property
    def id(self):
        """Entry ID generated from URL."""
        return urn_from_string(self.raw_entry['loc'])

    @property
    def updated(self):
        """Lastmod time of entry with fallback on publish times of video and news extensions."""
        return process_time(self.raw_entry.get('lastmod')
                            or self.raw_entry.get('video', {}).get('publication_date')
                            or self.raw_entry.get('news', {}).get('publication_date'),
                            default_tz=self.fetcher.default_tz)

    @property
    def link(self):
        """Sitemap entry location (i.e. the URL)."""
        return self.raw_entry['loc']


class SitemapFetcher(BaseFetcher):
    """
    Fetcher that supports sitemaps and recognizes some features of some sitemap extensions.
    """

    EntryInterface = SitemapEntryInterface

    @staticmethod
    @stopwatch
    def parse(response):
        """Return parsed sitemap."""
        return Sitemap(response.content)

    def update(self):
        """Process sitemap."""
        response = self.retrieve()
        self.raw_entries = self.parse(response)

    @property
    def id(self):
        """Sitemap ID generated from explicitly set URL."""
        return urn_from_string(self.url)


class SitemapIndexFetcher(BaseFetcher):
    """
    This entry point that distributes the sitemap URLs in a sitemap index on
    individual sitemap fetchers is still a bit of a hack. It only supports one
    level of sitemap indices and circumvents the request scheduling, so that
    it can block the scheduler for a while and sends many consecutive requests
    to the same host.
    """

    EntryInterface = SitemapEntryInterface
    SitemapFetcher = SitemapFetcher

    def __init__(self, *args, **kwargs):
        super(SitemapIndexFetcher, self).__init__(*args, **kwargs)
        self.response_headers = {}
        self.index = None
        self.urls = []

    @stopwatch
    def parse(self, response):
        """Parse the sitemap index."""
        return SitemapIndex(response.content)

    def clean(self):
        """Reset the fetcher."""
        self.index = None

    def update(self):
        """Run the retrieval cycle that calls the sitemap fetcher internally."""
        response = self.retrieve()
        self.index = self.parse(response)
        self.urls = []
        for sitemap in self.index:
            if 'lastmod' in sitemap:
                sitemap['lastmod'] = dateutil.parser.parse(sitemap['lastmod'], ignoretz=True)
                if sitemap['lastmod'] < datetime.utcnow() - settings.PAST:
                    continue
            try:
                response = self._retrieve_sitemap(sitemap['loc'])
            except (IOError, requests.RequestException) as excp:
                logger.error('Request exception %r for %s in index %s',
                             excp, sitemap['loc'], self.url)
            except UnchangedException:
                logger.info('Sitemap unchanged')
            else:
                self.urls.extend(self.SitemapFetcher.parse(response))

    @property
    def id(self):
        """Unique ID of the sitemap generated from explicitly set URL."""
        return urn_from_string(self.url)

    def _retrieve_sitemap(self, url):
        """Wrapper around the requests library for retrieving sitemap indices."""
        self.kwargs['headers'].update(canonicalized({
            'if-modified-since': self.response_headers.get('last-modified'),
            'if-none-match': self.response_headers.get('etag')}))
        response = requests.get(url, **self.kwargs)
        response.raise_for_status()
        if response.url != url:
            logger.info('Redirects to %s', response.url)
        if response.status_code == 304:
            raise UnchangedException
        self.response_headers[url] = response.headers
        return response

    @property
    def raw_entries(self):
        """The raw entries as returned by parser."""
        return self.urls
