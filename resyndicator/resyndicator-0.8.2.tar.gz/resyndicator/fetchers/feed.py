import json
import warnings
from datetime import datetime, timedelta
from urllib.parse import parse_qsl, urlparse

import feedparser
from cached_property import cached_property

from ..utils import (decode_response, fixed_text, process_time, stopwatch,
                     urn_from_string)
from .base import BaseEntryInterface, BaseFetcher


class FeedEntryInterface(BaseEntryInterface):

    @cached_property
    def updated(self):
        """The time the entry was last updated on the server side."""
        now = datetime.utcnow()
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            # It tells us not to rely on these two fields’ always being present.
            # But we don’t anyway.
            # https://pythonhosted.org/feedparser/reference-feed-updated.html
            raw_updated = self.raw_entry.get('updated_parsed') \
                or self.raw_entry.get('updated')
        raw_published = self.raw_entry.get('published_parsed') \
            or self.raw_entry.get('published')
        updated = process_time(
            raw_updated, default_tz=self.fetcher.default_tz)
        published = process_time(
            raw_published, default_tz=self.fetcher.default_tz)
        # Correct implausible dates, with one day tolerance due to possible TZ errors
        updated = updated if not updated or updated < now + timedelta(days=1) else now
        published = published if not published or published < now + timedelta(days=1) else now
        if updated and published:
            # Wordpress, notably, does not treat publishing as update,
            # which may cause articles schedule some time ago to pop up
            # too far in the past to make it onto the feed.
            updated = max(updated, published)
        return updated or published or now

    @cached_property
    def published(self):
        """The time the entry was published."""
        now = datetime.utcnow()
        raw_date = self.raw_entry.get('published_parsed') or self.raw_entry.get('published')
        published = process_time(
            raw_date, default_tz=self.fetcher.default_tz)
        published = published if not published or published < now + timedelta(days=1) else now
        return published

    @cached_property
    def id(self):
        """
        The GUID of an Atom feed or an ID generated from updated date, link, title, and summary
        if we run into an RSS feed without ID. This is bound to incur duplicates if one of these
        data changes, but that’s better than filtering out actually unique entries.
        """
        if 'id' in self.raw_entry:
            return self.raw_entry['id']
        # “… at least one of title or description must be present.”
        # http://www.rssboard.org/rss-specification/
        return urn_from_string((self.link or '') + (self.title or self.summary or ''))

    @cached_property
    def source(self):
        """
        The raw dict as feedparser returns it as JSON string inside an HTML snippet
        to be appended to the entry content.
        """
        entry = {key: value for key, value in self.raw_entry.items()
                 if key not in ('summary', 'summary_detail', 'content')}
        return ('<details>\n'
                '<summary>JSON Source</summary>\n'
                '<div class="entry-source">{}</div>\n'
                '</details>').format(json.dumps(
                    entry, indent=4, sort_keys=True, default=str))

    @cached_property
    @fixed_text()
    def content(self):
        """The entry content as a single string if present."""
        content = '\n\n'.join(
            content.get('value', '')
            for content in self.raw_entry.get('content', [])).strip()
        return content or None

    @cached_property
    def content_type(self):
        """The entry content type (text or html). Defaults to text."""
        # Ignores default if content missing. That’s correct, I think.
        if 'content' in self.raw_entry:
            return self.fetcher.type_mapping.get(
                self.raw_entry['content'][0]['type'], 'text')

    @cached_property
    @fixed_text()
    def title(self):
        """The title of the entry."""
        return self.raw_entry.get('title')

    @cached_property
    def link(self):
        """The entry link."""
        link = self.raw_entry.get('link')
        if link and ('&url=http' in link or '?url=http' in link):
            # Google and Bing like to use tracking URLs that degrade the deduplication
            link = dict(parse_qsl(urlparse(link).query)).get('url', link)
        return link

    @cached_property
    @fixed_text()
    def summary(self):
        """The entry summary. None if identical to content."""
        summary = self.raw_entry.get('summary', '').strip()
        if summary == self.content:
            return
        return summary or None

    @cached_property
    def summary_type(self):
        """The entry summary type (text or html). Defaults to text."""
        # See above.
        if 'summary_detail' in self.raw_entry:
            return self.fetcher.type_mapping.get(
                self.raw_entry['summary_detail']['type'], 'text')

    @cached_property
    @fixed_text()
    def author(self):
        """The entry author."""
        return '; '.join([author['name']
                          for author in self.raw_entry.get('authors', [])
                          if 'name' in author]) \
               or self.raw_entry.get('author')


class FeedFetcher(BaseFetcher):

    EntryInterface = FeedEntryInterface
    type_mapping = {
        'text/plain': 'text',
        'text/html': 'html',
        'application/xhtml+xml': 'xhtml'}

    @stopwatch
    def parse(self, response):
        """Decode and parse the feed and return the result."""
        raw_feed = decode_response(response)
        # This issue introduces encoding errors:
        # http://code.google.com/p/feedparser/issues/detail?id=378
        # This issue leads to broken URLs:
        # http://code.google.com/p/feedparser/issues/detail?id=357
        return feedparser.parse(raw_feed)

    def update(self):
        """Update the list of unprocessed entries."""
        response = self.retrieve()
        self.source = self.parse(response)
        self.raw_entries = self.source.entries

    @cached_property
    def id(self):
        """Unique ID for the feed. Generated from link or title if missing."""
        if 'id' in self.source.feed:
            return self.source.feed['id']
        return urn_from_string(
            self.source.feed.get('link', self.source.feed.get('title', '')))

    @cached_property
    @fixed_text()
    def title(self):
        """The feed title."""
        return self.source.feed.get('title')

    @cached_property
    @fixed_text()
    def subtitle(self):
        """The subtitle of the feed."""
        return self.source.feed.get('subtitle')

    @cached_property
    def link(self):
        """
        The link pointing to the feed. Not used for the `source_link` attribute because the
        feed URL might redirect in unpredictable ways while the first URL in the chain is
        explicitly known.
        """
        return self.source.feed.get('link')

    @cached_property
    def hub(self):
        """Hub (such as PubSubHubbub) of the feed, if any."""
        for link in self.source.get('links', []):
            if link.get('rel') == 'hub':
                return link['href']

    @cached_property
    @fixed_text()
    def author(self):
        """Author of the feed, or one string listing all authors."""
        return '; '.join([author['name']
                          for author in self.source.feed.get('authors', [])
                          if 'name' in author]) \
               or self.source.feed.get('author')

    @cached_property
    @fixed_text()
    def generator(self):
        """The feed generator."""
        return self.source.feed.get('generator')
