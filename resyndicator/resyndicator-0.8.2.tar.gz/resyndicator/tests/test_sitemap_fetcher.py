import pytest
from datetime import datetime
from ..fetchers.sitemap import SitemapFetcher, SitemapIndexFetcher


class MockSitemapFetcher(SitemapFetcher):

    def __init__(self, url, *args, **kwargs):
        super().__init__(url, 60, *args, **kwargs)
        self.update()

    def update(self):
        with open('resyndicator/tests/samples/' + self.url, 'rb') as xmlfile:
            content = xmlfile.read()
        self.raw_entries = self.parse(type('response', (), {'content': content}))


class MockSitemapIndexFetcher(SitemapIndexFetcher):

    def __init__(self, url, *args, **kwargs):
        super().__init__(url, 60, *args, **kwargs)
        self.update()

    def update(self):
        with open('resyndicator/tests/samples/' + self.url, 'rb') as xmlfile:
            content = xmlfile.read()
        self.index = self.parse(type('response', (), {'content': content}))


fetchers = {
    'sitemap.xml': MockSitemapFetcher('sitemap.xml'),
    'sitemap-index.xml': MockSitemapIndexFetcher('sitemap-index.xml'),
}


@pytest.mark.parametrize('fetcher', [
    fetchers['sitemap.xml'],
    fetchers['sitemap-index.xml'],
])
def test_parsing(fetcher):
    for entry in fetcher.entries:
        assert entry.id  # Just to prove that the entry has been parsed


@pytest.mark.parametrize('fetcher,updated', [
    (fetchers['sitemap.xml'], datetime(2006, 11, 18, 0, 0)),
])
def test_updated_dates(fetcher, updated):
    assert next(fetcher.entries).updated == updated


@pytest.mark.parametrize('fetcher,link', [
    (fetchers['sitemap.xml'], 'http://example.com/?foo=bar&query=string'),
])
def test_links(fetcher, link):
    assert next(fetcher.entries).link == link


@pytest.mark.parametrize('fetcher,id', [
    (fetchers['sitemap.xml'], 'urn:uuid:564746c7-772c-fa89-0cda-6fd768655517'),
])
def test_ids(fetcher, id):
    assert fetcher.id
    assert next(fetcher.entries).id == id
