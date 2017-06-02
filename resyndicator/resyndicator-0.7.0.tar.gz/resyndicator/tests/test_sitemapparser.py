import pytest
from ..utils.sitemapparser import Sitemap, SitemapIndex


with open('resyndicator/tests/samples/sitemap.xml', 'rb') as xmlfile:
    sitemap = Sitemap(xmlfile.read())
with open('resyndicator/tests/samples/sitemap-index.xml', 'rb') as xmlfile:
    sitemapindex = SitemapIndex(xmlfile.read())


@pytest.mark.parametrize('parser,field,value', [
    (sitemap, 'loc', 'http://example.com/?foo=bar&query=string'),
    (sitemap, 'lastmod', '2006-11-18'),
    (sitemap, 'changefreq', 'daily'),
    (sitemap, 'priority', '0.8'),
])
def test_sitemap(parser, field, value):
    assert next(iter(parser))[field] == value


@pytest.mark.parametrize('parser,field,value', [
    (sitemapindex, 'loc', 'http://www.example.com/sitemap1.xml.gz'),
    (sitemapindex, 'lastmod', '2014-10-01T18:23:17+00:00'),
])
def test_sitemapindex(parser, field, value):
    assert next(iter(parser))[field] == value
