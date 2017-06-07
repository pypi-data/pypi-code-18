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
    """Indicates that a feed or sitemap has not been changed."""
    pass


class BaseEntryInterface(object):
    """
    Base class for entries.

    Subclass this to provide a unified interface to any type of entry
    you want to import.
    """

    Entry = Entry

    def __init__(self, fetcher, raw_entry):
        self.fetcher = fetcher
        self.raw_entry = raw_entry

    @property
    def id(self):
        """
        A globally unique ID for internal deduplication
        and identification by feed readers
        """
        pass

    @property
    def summary(self):
        """Summary or description of the entry"""
        pass

    @property
    def summary_type(self):
        """Either `text` or `html` (important for the Atom output)"""
        pass

    @property
    def content(self):
        """Full content of the entry if given"""
        pass

    @property
    def content_type(self):
        """Either `text` or `html` (important for the Atom output)"""
        pass

    @property
    def source(self):
        """
        Optional field to insert any entry source code into the
        content field. This can be set through `settings.INCLUDE_SOURCE`.
        """
        pass

    @property
    def title(self):
        """Entry title"""
        pass

    @property
    def fetched(self):
        """Fetch time (set to `datetime.datetime.utcnow()` by default)"""
        return datetime.utcnow()

    @property
    def updated(self):
        """Time the entry was updated on the supplier side"""
        pass

    @property
    def published(self):
        """Time the entry was published"""
        pass

    @property
    def link(self):
        """Entry link"""
        pass

    @property
    def author(self):
        """Entry author"""
        pass

    def _new_entry(self):
        """
        Create new entry

        The methodology is such that an SQLAlchemy entry is created for each entry from the start.
        If it is a new entry, a new SQLAlchemy entry is created for it in memory but not yet
        committed. If it is an existing one, a mapped SQLAlchemy entry is created. A `created`
        attribute indicates which one is the case. This allows us to handle creations and
        updates almost the same without having to have two complete separate control flows
        for the cases.
        """
        entry = self.fetcher.session.query(self.Entry).filter_by(id=self.id).one_or_none()
        if not entry and settings.UNIQUE_LINKS:
            entry = self.fetcher.session.query(self.Entry) \
                .filter_by(link=self.link).order_by(Entry.updated).first()
        if not entry:
            entry = self.Entry()
            self.fetcher.session.add(entry)
            entry.created = True  # Marker for later updating
        return entry

    @property
    def entry(self):
        """
        Return the SQLAlchemy entry.

        Here, the `source` property is used to optionally include the entry source code
        (specified through `settings.INCLUDE_SOURCE`). If the entry exists, it is returned
        unchanged. Otherwise, it is initialized with all the new values from the supplier.
        """
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
    """
    Base class for fetchers.

    Subclass this to implement your own custom types of fetchers.
    """

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
        """A unique ID for the data source, e.g., the feed"""
        pass

    @property
    def title(self):
        """Title of the data source"""
        pass

    @property
    def subtitle(self):
        """Subtitle of the data source"""
        pass

    @property
    def link(self):
        """Link to the data source"""
        pass

    @property
    def hub(self):
        """Optionally the endpoint of a hub such as PubSubHubbub"""
        pass

    @property
    def author(self):
        """The author of the data source"""
        pass

    @property
    def generator(self):
        """The generator of the data source"""
        pass

    def __hash__(self):
        return hash(self.url)

    def retrieve(self):
        """
        Retrieve the data source.

        This is by default a wrapper around the requests library that sets headers such that
        servers can indicate that the content hasn’t changed since the last retrieval, and
        by default also specifies a custom user agent and timeout.
        """
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
        """
        Implement this function to convert your data source to something the `update` method
        can work with.
        """
        raise NotImplementedError()

    @property
    def needs_update(self):
        """Return whether the source is ripe for an update."""
        return self.next_check < time.time()

    @property
    def next_check(self):
        """The time of the next update."""
        return self.last_check + self.interval

    def touch(self):
        """Set the time of the last check of the source to the current time."""
        self.last_check = time.time()

    def clean(self):
        """Reset the fetcher."""
        self.source = None
        self.raw_entries = None

    def is_valid(self, entry):
        """Test the validity of an entry. Only returns `True` by default."""
        return True

    @property
    def entries(self):
        """Yield the SQLAlchemy entries after setting any default values."""
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
        """
        Commit the entries or any updates to them to the database and return
        the entries that have been created."""
        entries = list(self.entries)  # Entries created in generator
        self.session.commit()
        fresh_entries = [entry for entry in entries if entry.created]
        if fresh_entries:
            logger.info('%s new entries', len(fresh_entries))
        return fresh_entries
