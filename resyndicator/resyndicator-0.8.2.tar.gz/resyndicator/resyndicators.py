from datetime import datetime
from operator import attrgetter

import requests

import xmltodict
from slugify import slugify
from utilofies.stdlib import canonicalized, isoformat

from . import settings
from .models import DefaultSession, Entry
from .utils import FeedTemplate, urn_from_string, stopwatch
from .utils.clustering import Clustering
from .utils.logger import logger


class Resyndicator(object):
    """
    The Resyndicator class represents a feed that is generated from the retrieved data on
    the bases of an SQLAlchemy query. It is identified by the title that you sepecify on
    instantiation, so do not change it, because that’ll be tantamount to creating a new
    resyndicator.
    """

    Entry = Entry

    def __init__(self, title, query, session=DefaultSession, past=None,
                 length=settings.DEFAULT_LENGTH, cluster_level=None, **kwargs):
        """
        :param title: Title of the resyndicator. This identifies the resyndicator,
            so do not change it unless your goal is to create a new resyndicator.

        :param query: SQLAlchemy filter statement to select the entries that should
            make up the resyndicated feed.

        :param session: (Optional) Change to supply your own database session for
            the resyndicator to use.

        :param past: (Optional) The timedelta used as cutoff for the feed.
            Older entries are ignored.

        :param length: (Optional) The maximum length of the feed.

        :param cluster_level: (Optional) The distance treshold that determines
            if two items are to be put in a cluster or not. A large value means
            that even not so similar items belong to one cluster, small value
            groups only very similar members. For example: for a set of
            20 members a value of 0.4 produce 7 2-3 item clusters, while
            a value of 0.8 gives 3 5-10 item clusters. Set to None by default,
            deactivating clustering altogether.

        :param **kwargs: Additional feed-level meta data.
        """
        self.title = title  # Don't change it
        self.slug = slugify(title, to_lower=True)
        self.length = length
        self.metadata = kwargs
        self.id = urn_from_string(self.title)
        self.query = query
        self.past = past
        self.cluster_level = cluster_level
        self.url = '{}{}.atom'.format(settings.BASE_URL, self.slug)
        self.session = session()

    @stopwatch
    def entries(self):
        """Query all relevant entries from the database."""
        query = self.session.query(self.Entry)
        if self.past:
            query = query.filter(self.Entry.updated > datetime.utcnow() - self.past)
        entries = query.filter(self.query) \
            .order_by(self.Entry.updated.desc())[:self.length * 10]  # Hopefully long enough
        if self.cluster_level is not None:
            clusters = Clustering.clustered(
                iterable=entries, level=self.cluster_level, key=lambda entry: entry.title)
            entries = [entries[-1] for entries in clusters[:self.length]]
        return entries

    def feed(self):
        """Generate the serialized feed."""
        # Long-running function. I’ve seen it take 13 s to complete.
        entries = self.entries()
        feed = FeedTemplate.feed()
        feed['feed']['id'] = self.id
        feed['feed']['title'] = self.title
        feed['feed']['updated'] = isoformat(entries[0].updated) if entries else None
        feed['feed']['link'][0]['@href'] = self.url
        feed['feed'].update(self.metadata)
        for entry in entries[:self.length]:
            feed_entry = FeedTemplate.entry()
            feed_entry['id'] = urn_from_string(entry.id)
            feed_entry['updated'] = isoformat(entry.updated)
            feed_entry['published'] = isoformat(entry.published)
            feed_entry['title'] = entry.title
            feed_entry['author']['name'] = entry.author
            feed_entry['link']['@href'] = entry.link
            feed_entry['summary']['@type'] = entry.summary_type
            feed_entry['summary']['#text'] = entry.summary
            feed_entry['content']['@type'] = entry.content_type
            feed_entry['content']['#text'] = entry.content
            feed_entry['source']['id'] = entry.source_id
            feed_entry['source']['title'] = entry.source_title
            feed_entry['source']['link']['@href'] = entry.source_link
            feed['feed']['entry'].append(feed_entry)
        feed = canonicalized(feed, blacklist=(None, '', {}))
        return xmltodict.unparse(feed, pretty=True)

    def publish(self):
        """Write the serialized feed to a file."""
        # Generate the serialized feed first, because Python empties the file
        # before it writes to it, so for the duration of the write, it stays
        # empty. This duration should be as short as we can make it.
        feed = self.feed()
        with open(settings.WEBROOT + self.slug + '.atom',
                  encoding='utf-8', mode='w') as feedfile:
            feedfile.write(feed)

    def pubsub(self, fresh_entries):
        """Publish new entries to a hub like PubSubHubbub."""
        if not settings.HUB or not fresh_entries:
            # Skip if PubSubHubbub is deactivated or there are no new entries
            return
        entry_ids = set(map(attrgetter('id'), self.get_entries()))
        fresh_entry_ids = set(map(attrgetter('id'), fresh_entries))
        if entry_ids & fresh_entry_ids:
            logger.info('Publishing %s to %s', self.title, settings.HUB)
            try:
                response = requests.post(
                    settings.HUB,
                    data={'hub.mode': 'publish', 'hub.url': self.url})
            except (IOError, requests.RequestException) as excp:
                logger.error('Request exception %r for %s while publishing %s',
                             excp, settings.HUB, self.title)
            else:
                if response.status_code != 204:
                    logger.error('Publishing %s to %s failed: %s',
                                 self.title, settings.HUB, response.text)
