import json
import time
from datetime import datetime
from operator import attrgetter, itemgetter
from random import randrange

from birdy.twitter import UserClient, StreamClient
from dateutil.parser import parse as parse_date
from dateutil.tz import tzutc
from utilofies.stdlib import itertimeout, sub_slices, cached_property

from .. import settings
from .base import BaseFetcher, BaseEntryInterface
from ..models import Entry, DefaultSession
from ..utils.logger import logger


class TweetInterface(BaseEntryInterface):
    """Mapping for individual tweets."""

    Entry = Entry

    @property
    def tweet_text(self):
        """Assemble a presentable text respresentation of the tweet."""
        if 'retweeted_status' in self.raw_entry:
            tweet = self.raw_entry['retweeted_status']
            prefix = 'RT @{screen_name}: '.format(
                screen_name=tweet['user']['screen_name'])
        else:
            tweet = self.raw_entry
            prefix = ''
        replacements = {}
        for url in tweet['entities']['urls']:
            replacements[tuple(url['indices'])] = \
                url.get('display_url', url['expanded_url'])
        for medium in tweet['entities'].get('media', []):
            replacements[tuple(medium['indices'])] = \
                medium.get('display_url', medium['expanded_url'])
        # Purging possible None values
        replacements = {key: value for key, value in replacements.items() if value}
        return prefix + sub_slices(tweet['text'], replacements)

    @property
    def tweet_html(self):
        """Assemble a presentable HTML respresentation of the tweet."""
        # TODO: Embed replies
        if 'retweeted_status' in self.raw_entry:
            tweet = self.raw_entry['retweeted_status']
            prefix = (
                'RT <a href="https://twitter.com/{screen_name}"'
                ' title="{name}">@{screen_name}</a>: ').format(
                    screen_name=tweet['user']['screen_name'],
                    name=tweet['user']['name'])
        else:
            tweet = self.raw_entry
            prefix = ''
        images = []
        replacements = {}
        for url in tweet['entities']['urls']:
            replacements[tuple(url['indices'])] = (
                '<a href="{expanded_url}">{display_url}</a>'.format(
                    expanded_url=url['expanded_url'],
                    display_url=url.get('display_url',
                                        url['expanded_url'])))
            if any(map((url['expanded_url'] or '').endswith,
                       ('.png', '.jpg', '.jpeg', '.gif', '.svg'))):
                images.append(url['expanded_url'])
        for hashtag in tweet['entities']['hashtags']:
            replacements[tuple(hashtag['indices'])] = (
                ('<a href="https://twitter.com/#!/search/'
                 '?q=%23{hashtag}&src=hash">#{hashtag}</a>').format(
                    hashtag=hashtag['text']))
        for mention in tweet['entities']['user_mentions']:
            # Case insensitive
            verbatim = tweet['text'][slice(*mention['indices'])]
            replacements[tuple(mention['indices'])] = (
                ('<a href="https://twitter.com/{screen_name}" title="{name}">'
                 '{verbatim}</a>').format(
                    screen_name=mention['screen_name'],
                    name=mention['name'],
                    verbatim=verbatim))
        for medium in tweet['entities'].get('media', []):
            replacements[tuple(medium['indices'])] = (
                '<a href="{expanded_url}">{display_url}</a>'.format(
                    expanded_url=medium['expanded_url'],
                    display_url=medium.get('display_url',
                                           medium['expanded_url'])))
            if medium['type'] == 'photo':
                images.append(medium['media_url'])
        # Purging possible None values
        replacements = {key: value for key, value in replacements.items() if value}
        text = prefix + sub_slices(tweet['text'], replacements)
        images = '<br />'.join('<img src="{url}" alt="" />'.format(url=url)
                               for url in images)
        return '<p>{text}</p><p>{images}</p>'.format(text=text, images=images)

    @property
    def id(self):
        """The tweet ID as string."""
        return str(self.raw_entry['id'])

    @property
    def fetched(self):
        """Time the tweet was fetched."""
        return datetime.utcnow()

    @property
    def updated(self):
        """Time the tweet was created."""
        date = parse_date(self.raw_entry['created_at'])
        return date.astimezone(tzutc()).replace(tzinfo=None)

    @property
    def title(self):
        """Optionally shortened representation of the tweet text."""
        tweet_text = self.tweet_text
        max_length = settings.TWITTER_TITLE_LENGTH
        if max_length and len(tweet_text) > max_length:
            return tweet_text[:max_length - 1] + '…'
        return tweet_text

    @property
    def author(self):
        """The tweep."""
        return '{screen_name} ({name})'.format(
            screen_name=self.raw_entry['user']['screen_name'],
            name=self.raw_entry['user']['name'])

    @property
    def link(self):
        """The URL of the tweet."""
        return 'https://twitter.com/{screen_name}/statuses/{id}'.format(
            screen_name=self.raw_entry['user']['screen_name'],
            id=self.raw_entry['id'])

    @property
    def content(self):
        """The HTML representation of the tweet."""
        return self.tweet_html

    @property
    def source_id(self):
        """URN to identify the tweep."""
        return 'urn:twitter:user:{id}'.format(id=self.raw_entry['user']['id'])

    @property
    def source_title(self):
        """Some generated source title based on the author name."""
        return '{author} on Twitter'.format(author=self.author)

    @property
    def source_link(self):
        """Link to the Twitter account of the author."""
        return 'https://twitter.com/{screen_name}'.format(
            screen_name=self.raw_entry['user']['screen_name'])

    @property
    def entry(self):
        """The SQLAlchemy entry representing the tweet."""
        entry = super().entry
        if entry.created:
            entry.published = self.updated
            entry.source_id = self.source_id
            entry.source_title = self.source_title
            entry.source_link = self.source_link
        return entry


class TwitterFetcher(BaseFetcher):

    EntryInterface = TweetInterface
    count = 200
    url = 'https://twitter.com/'  # For consistency

    def __init__(self, oauth_token, oauth_secret, interval,
                 session=DefaultSession, default_tz=tzutc, defaults=None):
        self.client = UserClient(
            settings.CONSUMER_KEY, settings.CONSUMER_SECRET,
            oauth_token, oauth_secret)
        self.defaults = defaults or {}
        # Fuzziness to spread updates out more evenly
        self.interval = interval - randrange(interval // 10 + 1)
        self.last_check = time.time() + self.interval
        self.default_tz = default_tz
        self.session = session()

    @cached_property
    def profile(self):
        """The profile of the Twitter user."""
        response = self.client.api.account.verify_credentials.get(skip_status=True)
        return response.data

    def __str__(self):
        return '@{} on Twitter'.format(self.profile.screen_name)

    def update(self):
        """Retrieve the current set of tweets."""
        response = self.client.api.statuses.home_timeline.get(
            count=self.count, exclude_replies=False, include_entities=True)
        self.raw_entries = response.data


class TwitterStreamer:
    """
    A Twitter streaming client that doesn’t work at the moment due to an error in
    the Birdy library. Please use the TwitterFetcher in the meantime.
    """

    def __init__(self, oauth_token, oauth_secret, session=DefaultSession, timeout=0, **kwargs):
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_secret
        self.timeout = timeout
        self.kwargs = kwargs
        self.friends = None
        self.client = StreamClient(
            settings.CONSUMER_KEY,
            settings.CONSUMER_SECRET,
            settings.OAUTH_TOKEN,
            settings.OAUTH_SECRET)
        self.session = session()

    def store(self, entries, new=False):
        if not new:
            existing_ids = map(
                itemgetter(0),
                self.session.query(self.TweetInterface.Entry.id)
                    .filter(self.TweetInterface.Entry.id.in_(
                        map(attrgetter('id'), entries))))
            entries = [entry for entry in entries
                       if entry.id not in existing_ids]
        try:
            for entry in entries:
                self.session.merge(entry)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return entries

    def retrieve_home_timeline(self, count=200):
        return self.rest.get_home_timeline(
            count=count, exclude_replies=False, include_entities=True)

    def run(self):
        for i, tweet in enumerate(itertimeout(
                self.client.userstream.user.get(**{'replies': 'all', 'with': 'followings'}),
                timeout=self.timeout)):
            fresh_entries = []
            if i % settings.TWITTER_STREAM_GET_INTERVAL == 0:
                # i == 0: Initial fetch in case we missed something
                # i != 0: Additional fetch in case the streaming API
                #         missed something.
                try:
                    get_tweets = self.retrieve_home_timeline()
                except Exception as excp:
                    logger.exception('Error during initial fetch: %r', excp)
                else:
                    entries = [TweetInterface(get_tweet).entry
                               for get_tweet in get_tweets]
                    fresh_entries = self.store(entries)
                    logger.info(
                        'Stored %s missed tweets by %s',
                        len(fresh_entries),
                        ', '.join(entry.author for entry in fresh_entries)
                        or 'everyone')
            logger.debug(json.dumps(tweet, indent=4))
            if 'id' in tweet:
                if tweet['user']['id'] in self.friends:
                    entry = TweetInterface(tweet).entry
                    self.store([entry], new=True)
                    logger.info('Stored tweet %s by %s',
                                tweet['id'], tweet['user']['screen_name'])
                    fresh_entries.append(entry)
                else:
                    # Unfortunately Twitter also streams replies to tweets by
                    # people we’re following regardless of whether we’re
                    # following the author.
                    logger.info('Skipping foreign tweet by %s',
                                tweet['user']['screen_name'])
            elif 'friends' in tweet:
                # Should be the first item to be streamed
                self.friends = tweet['friends']
                logger.info('Received list of %s friends',
                            len(tweet['friends']))
            elif tweet.get('event') == 'follow':
                self.friends.append(tweet['target']['id'])
                logger.info('Received follow event for %s',
                            tweet['target']['screen_name'])
            else:
                logger.info('Skipping weird object: %s', tweet)
            # Final yield
            if fresh_entries:
                yield fresh_entries
