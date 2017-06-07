import requests
from copy import copy
from datetime import datetime
from urllib.parse import urlparse
from lxml.etree import LxmlError
from sqlalchemy.sql import or_
from readability import Document
from readability.readability import Unparseable
from ..utils import decode_response
from ..utils.logger import logger
from ..models import Entry, DefaultSession
from .. import settings


class ContentFetcher(object):
    """
    Fetcher class for retrieval and extraction of content from websites.

    This fetcher incrementally downloads and extracts (using Readability)
    the content from any pages associated with entries that don’t already
    have long-form content associated with them.
    """

    Entry = Entry

    def __init__(self, session=DefaultSession, past=None, **kwargs):
        self.past = past
        self.session = session()
        self.stub_entries = []
        self.entries = []
        self.kwargs = kwargs
        self.kwargs.setdefault('headers', {})
        self.kwargs['headers'].setdefault('user-agent', settings.USER_AGENT)
        self.kwargs.setdefault('timeout', settings.TIMEOUT)

    def update(self):
        """Replenish the in-memory list of entries to process."""
        query = self.session.query(self.Entry) \
            .filter(or_(self.Entry.content==None, self.Entry.content==''),
                    self.Entry.link!=None)
        if self.past:
            query = query.filter(self.Entry.updated > datetime.utcnow() - self.past)
        # Sorted newest first so that if content vanishes we at least get to
        # fetch some of it. Minimal risk rather than all or nothing.
        self.stub_entries = query.order_by(self.Entry.updated.desc()).all()

    @staticmethod
    def get_hostname(entry):
        """
        Wrapper for extrating the hostname from entry links.
        (Another ContentFetcher might need to remove the `.www`.)
        """
        # For subclassing for different entry types
        return urlparse(entry.link).hostname

    def select(self):
        """
        Return a list of entries where there is only one per host so to
        maximize the time between requests to the same host.
        """
        known_hosts = set()
        for entry in copy(self.stub_entries):
            hostname = self.get_hostname(entry)
            if hostname not in known_hosts:
                known_hosts.add(hostname)
                self.stub_entries.remove(entry)
                yield entry

    def _fetch(self, url):
        """Retrieve the unprocessed web page."""
        response = requests.get(url, **self.kwargs)
        response.raise_for_status()
        return response

    def _decode(self, response):
        """Decode the response."""
        return decode_response(response)

    def _extract(self, html, url):
        """Use Readability to extract the main content of the page."""
        return Document(html, url=url)

    def _enrich(self, entry, document):
        """Extend the entry with content from the extraction."""
        entry.content = document.summary()
        entry.content_type = 'html'
        if not entry.title or not entry.title.strip():
            entry.title = document.short_title()
        return entry

    def fetch(self):
        """
        Run one full fetching cycle. This is the main entry point for the content fetching process.
        """
        if not self.stub_entries:
            self.update()
            if not self.stub_entries:
                return
        logger.info('%s entries queued', len(self.stub_entries))
        for entry in self.select():
            logger.info('Fetching %s', entry.link)
            try:
                response = self._fetch(entry.link)
            except (IOError, requests.RequestException) as excp:
                logger.error('Request exception %r', excp)
                entry.content = 'Request exception {!r}'.format(excp)
                entry.content_type = 'text'
                continue
            try:
                html = self._decode(response)
                document = self._extract(html, url=response.url)
                entry = self._enrich(entry, document)  # Exceptions were typically raised here
            except (LxmlError, Unparseable) as excp:
                logger.error('Parser exception %r', excp)
                entry.content = 'Parser exception {!r}'.format(excp)
                entry.content_type = 'text'
                continue
            self.entries.append(entry)

    def persist(self):
        """Commit the updates to the entries."""
        # Actually no need to access self.entries again
        self.session.commit()
        self.entries = []
