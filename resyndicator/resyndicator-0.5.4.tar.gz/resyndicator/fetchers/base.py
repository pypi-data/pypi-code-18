import socket
import time
import requests
from random import randrange
from datetime import datetime
from dateutil.tz import tzutc
from utilofies.stdlib import canonicalized
from .. import settings
from ..utils.logger import logger
from ..models import Entry, DefaultSession


# In accordance with
# https://dev.twitter.com/docs/streaming-apis/connecting#Stalls
socket.setdefaulttimeout(90)


class UnchangedException(Exception):
    pass


class BaseEntryInterface(object):

    Entry = Entry

    def __init__(self, fetcher, raw_entry):
        self.fetcher = fetcher
        self.raw_entry = raw_entry

    @property
    def id(self):
        pass

    @property
    def summary(self):
        pass

    @property
    def summary_type(self):
        pass

    @property
    def content(self):
        pass

    @property
    def content_type(self):
        pass

    @property
    def source(self):
        pass

    @property
    def title(self):
        pass

    @property
    def fetched(self):
        return datetime.utcnow()

    @property
    def updated(self):
        pass

    @property
    def published(self):
        pass

    @property
    def link(self):
        pass

    @property
    def author(self):
        pass

    def _new_entry(self):
        entry = self.fetcher.session.query(self.Entry).filter_by(id=self.id).one_or_none()
        if not entry:
            entry = self.Entry()
            self.fetcher.session.add(entry)
            entry.created = True  # Marker for later updating
        return entry

    @property
    def entry(self):
        summary, summary_type = self.summary, self.summary_type
        content, content_type = self.content, self.content_type
        if settings.INCLUDE_SOURCE:
            if content:
                content = '{}\n\n{}'.format(content, self.source)
                content_type = 'html'
            else:
                # It is recommended that summary be nonempty
                # if there is no content. This is also useful
                # for the separate content fetching.
                summary = '{}\n\n{}'.format(summary, self.source)
                summary_type = 'html'
        entry = self._new_entry()
        if entry.created:
            entry.id = self.id
            entry.title = self.title or self.fetcher.title
            entry.fetched = self.fetched
            entry.updated = self.updated or datetime.utcnow()
            entry.published = self.published
            entry.link = self.link or self.fetcher.link or self.fetcher.url
            entry.summary = summary
            entry.summary_type = summary_type
            entry.content = content
            entry.content_type = content_type
            entry.author = self.author or self.fetcher.author
            entry.source_id = self.fetcher.id
            entry.source_title = self.fetcher.title
            entry.source_link = self.fetcher.url
        return entry


class BaseFetcher(object):

    type_mapping = {
        'text/plain': 'text',
        'text/html': 'html',
        'application/xhtml+xml': 'xhtml'}
    EntryInterface = BaseEntryInterface

    def __init__(self, url, interval, session=DefaultSession, default_tz=tzutc,
                 defaults=None, **kwargs):
        self.defaults = defaults or {}
        self.url = url
        # Fuzziness to spread updates out more evenly
        self.interval = interval - randrange(interval // 10 + 1)
        self.last_check = time.time() + self.interval
        self.default_tz = default_tz
        self.kwargs = kwargs
        self.kwargs.setdefault('headers', {})
        self.kwargs['headers'].setdefault('user-agent', settings.USER_AGENT)
        self.kwargs.setdefault('timeout', settings.TIMEOUT)
        self.response_headers = {}
        self.session = session()

    def __str__(self):
        return self.url

    @property
    def id(self):
        pass

    @property
    def title(self):
        pass

    @property
    def subtitle(self):
        pass

    @property
    def link(self):
        pass

    @property
    def hub(self):
        pass

    @property
    def author(self):
        pass

    @property
    def generator(self):
        pass

    def __hash__(self):
        return hash(self.url)

    def retrieve(self):
        self.kwargs['headers'].update(canonicalized({
            'if-modified-since': self.response_headers.get('last-modified'),
            'if-none-match': self.response_headers.get('etag')}))
        response = requests.get(self.url, **self.kwargs)
        response.raise_for_status()
        if response.url != self.url:
            logger.info('Redirects to %s', response.url)
        self.response_headers = response.headers
        if response.status_code == 304:
            raise UnchangedException
        return response

    def parse(self, response):
        raise NotImplementedError()

    @property
    def needs_update(self):
        return self.next_check < time.time()

    @property
    def next_check(self):
        return self.last_check + self.interval

    def touch(self):
        self.last_check = time.time()

    def clean(self):
        self.source = None
        self.raw_entries = None

    def is_valid(self, entry):
        return True

    @property
    def entries(self):
        for raw_entry in self.raw_entries:
            entry = self.EntryInterface(
                fetcher=self, raw_entry=raw_entry)
            if self.is_valid(entry):
                entry = entry.entry  # From EntryInterface to models.BaseEntry
                for key, value in self.defaults.items():
                    if not getattr(entry, key, None):
                        setattr(entry, key, value)
                yield entry

    def persist(self):
        entries = list(self.entries)  # Entries created in generator
        self.session.commit()
        fresh_entries = [entry for entry in entries if entry.created]
        if fresh_entries:
            logger.info('%s new entries', len(fresh_entries))
        return fresh_entries
