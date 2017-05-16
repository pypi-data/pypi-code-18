import json
import feedparser
from cached_property import cached_property
from ..utils import urn_from_string, stopwatch, decode_response, process_time
from .base import BaseEntryInterface, BaseFetcher


class FeedEntryInterface(BaseEntryInterface):

    @cached_property
    def updated(self):
        # Wordpress, notably, does not treat publishing as update,
        # which may cause articles schedule some time ago to pop up
        # too far in the past to make it onto the feed.
        raw_updated = self.raw_entry.get('updated_parsed') \
            or self.raw_entry.get('updated')
        raw_published = self.raw_entry.get('published_parsed') \
            or self.raw_entry.get('published')
        updated = process_time(
            raw_updated, default_tz=self.fetcher.default_tz)
        published = process_time(
            raw_published, default_tz=self.fetcher.default_tz)
        if updated and published:
            updated = max(updated, published)
        return updated or published

    @cached_property
    def published(self):
        raw_date = self.raw_entry.get('published_parsed') or self.raw_entry.get('published')
        return process_time(
            raw_date, default_tz=self.fetcher.default_tz)

    @cached_property
    def id(self):
        if self.raw_entry.has_key('id'):
            return self.raw_entry['id']
        # “… at least one of title or description must be present.”
        # http://www.rssboard.org/rss-specification/
        return urn_from_string(
            self.raw_entry.get('updated', '') +
            self.raw_entry.get('link', '') +
            self.raw_entry.get('title', self.raw_entry.get('summary', '')))

    @cached_property
    def source(self):
        entry = {key: value for key, value in self.raw_entry.items()
                 if key not in ('summary', 'summary_detail', 'content')}
        return ('<details>\n'
                '<summary>JSON Source</summary>\n'
                '<div class="entry-source">{}</div>\n'
                '</details>').format(json.dumps(
                    entry, indent=4, sort_keys=True, default=str))

    @cached_property
    def content(self):
        content = u'\n\n'.join(
            content.get('value', u'')
            for content in self.raw_entry.get('content', [])).strip()
        return content or None


    @cached_property
    def content_type(self):
        # Ignores default if content missing. That’s correct, I think.
        if self.raw_entry.has_key('content'):
            return self.fetcher.type_mapping.get(
                self.raw_entry['content'][0]['type'], 'text')

    @cached_property
    def title(self):
        return self.raw_entry.get('title')

    @cached_property
    def link(self):
        return self.raw_entry.get('link')

    @cached_property
    def summary_type(self):
        # See above.
        if self.raw_entry.has_key('summary_detail'):
            return self.fetcher.type_mapping.get(
                self.raw_entry['summary_detail']['type'], 'text')

    @cached_property
    def summary(self):
        summary = self.raw_entry.get('summary', '').strip()
        if summary == self.content:
            return
        return summary or None

    @cached_property
    def author(self):
        return '; '.join([author['name']
                          for author in self.raw_entry.get('authors', [])
                          if author.has_key('name')]) \
               or self.raw_entry.get('author')


class FeedFetcher(BaseFetcher):

    EntryInterface = FeedEntryInterface
    type_mapping = {
        'text/plain': 'text',
        'text/html': 'html',
        'application/xhtml+xml': 'xhtml'}

    @stopwatch
    def parse(self, response):
        raw_feed = decode_response(response)
        # This issue introduces encoding errors:
        # http://code.google.com/p/feedparser/issues/detail?id=378
        # This issue leads to broken URLs:
        # http://code.google.com/p/feedparser/issues/detail?id=357
        return feedparser.parse(raw_feed)

    def update(self):
        response = self.retrieve()
        self.source = self.parse(response)
        self.raw_entries = self.source.entries

    @cached_property
    def id(self):
        if self.source.feed.has_key('id'):
            return self.source.feed['id']
        return urn_from_string(
            self.source.feed.get('link', self.source.feed.get('title', '')))

    @cached_property
    def title(self):
        return self.source.feed.get('title')

    @cached_property
    def subtitle(self):
        return self.source.feed.get('subtitle')

    @cached_property
    def link(self):
        return self.source.feed.get('link')

    @cached_property
    def hub(self):
        for link in self.source.get('links', []):
            if link.get('rel') == 'hub':
                return link['href']

    @cached_property
    def author(self):
        return '; '.join([author['name']
                          for author in self.source.feed.get('authors', [])
                          if author.has_key('name')]) \
               or self.source.feed.get('author')

    @cached_property
    def generator(self):
        return self.source.feed.get('generator')
