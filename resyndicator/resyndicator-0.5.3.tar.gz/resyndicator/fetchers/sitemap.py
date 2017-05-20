import json
import requests
from utilofies.stdlib import canonicalized
from ..utils import urn_from_string, stopwatch, process_time
from ..utils.logger import logger
from ..utils.sitemapparser import SitemapIndex, Sitemap
from .base import BaseEntryInterface, BaseFetcher, UnchangedException


class SitemapEntryInterface(BaseEntryInterface):

    @property
    def source(self):
        return ('<details>\n'
                '<summary>JSON Source</summary>\n'
                '<div class="entry-source">{}</div>\n'
                '</details>').format(json.dumps(
                    self.raw_entry, indent=4, sort_keys=True, default=str))

    @property
    def id(self):
        return urn_from_string(self.raw_entry['loc'])

    @property
    def updated(self):
        return process_time(self.raw_entry.get('lastmod')
                or self.raw_entry.get('video', {}).get('publication_date')
                or self.raw_entry.get('news', {}).get('publication_date'),
            default_tz=self.fetcher.default_tz)

    @property
    def link(self):
        return self.raw_entry['loc']


class SitemapFetcher(BaseFetcher):

    EntryInterface = SitemapEntryInterface

    @staticmethod
    @stopwatch
    def parse(response):
        return Sitemap(response.content)

    def update(self):
        response = self.retrieve()
        self.raw_entries = self.parse(response)

    @property
    def id(self):
        return urn_from_string(self.url)


class SitemapIndexFetcher(BaseFetcher):

    EntryInterface = SitemapEntryInterface
    SitemapFetcher = SitemapFetcher

    def __init__(self, *args, **kwargs):
        super(SitemapIndexFetcher, self).__init__(*args, **kwargs)
        self.response_headers = {}

    @stopwatch
    def parse(self, response):
        return SitemapIndex(response.content)

    def clean(self):
        self.index = None

    def update(self):
        response = self.retrieve()
        self.index = self.parse(response)
        self.urls = []
        for sitemap in self.index:
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
        return urn_from_string(self.url)

    def _retrieve_sitemap(self, url):
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
        return self.urls
