import re
from xml.etree import cElementTree


namespace_re = re.compile('{[^}]*}')


class SitemapParsingException(Exception):
    pass


def dictify(element):
    """Convert an etree element to a dictionary."""
    return {str(child.tag): dictify(child) for child in element} \
        or str(element.text).strip()


def strip_namespaces(root):
    for element in root.iter():
        # Removing namespaces, sorry
        if isinstance(element.tag, str):
            # Sometimes <built-in function Comment>
            element.tag = namespace_re.sub('', element.tag)


class SitemapIndex:
    """Parser class for sitemap indices."""

    def __init__(self, xml):
        self.root = cElementTree.fromstring(xml)
        if self.root is None:
            raise SitemapParsingException('Unknown parsing error')
        strip_namespaces(self.root)
        self.sitemapindex = list(self._parse_sitemapindex(self.root))

    @staticmethod
    def _parse_sitemapindex(root):
        if not root.tag == 'sitemapindex':
            raise SitemapParsingException(
                'No sitemapindex found (tag: {tag})'.format(tag=root.tag))
        for sitemap in root:
            if not sitemap.tag == 'sitemap':
                continue
            entry = dictify(sitemap)
            if 'loc' not in entry:
                continue
            yield entry

    def __iter__(self):
        return iter(self.sitemapindex)


class Sitemap:
    """Parser class for sitemaps."""

    def __init__(self, xml):
        self.root = cElementTree.fromstring(xml)
        if self.root is None:
            raise SitemapParsingException('Unknown parsing error')
        strip_namespaces(self.root)
        self.urlset = list(self._parse_urlset(self.root))

    @staticmethod
    def _parse_urlset(root):
        if not root.tag == 'urlset':
            raise SitemapParsingException(
                'No urlset found (tag: {tag})'.format(tag=root.tag))
        for url in root:
            if not url.tag == 'url':
                continue
            entry = dictify(url)
            if 'loc' not in entry:
                continue
            yield entry

    def __iter__(self):
        return iter(self.urlset)
