import requests
import twitter
from twitter_controller.Text import Text
from requests import RequestException
from requests_oauthlib import OAuth1
from twitter import TwitterError

from ENV import APIs


class TwitterDownloader:

    passwords = APIs.tweeter

    def __init__(self):
        # seeting passwords for manual requests
        self.auth = OAuth1(*self.passwords)
        # setting passwords for library requests
        self.api = twitter.Api(*self.passwords)
        self.user = None

    def check_authentication(self):
        try:
            self.api.VerifyCredentials()
        except twitter.error.TwitterError:
            raise TwitterDownloaderException("Authentication validation failed")

    def set_twitteruser(self, name):
        try:
            [self.user] = self.api.GetUsersSearch(term=name, page=1, count=1, include_entities=None)
        except ValueError:
            raise TwitterDownloaderException('User not found')

    def get_profilepict_url(self):
        if self.user:
            return self.user.profile_image_url
        else:
            raise TwitterDownloaderException("You have to first set_twitteruser")

    def download_tweets(self, amount):
        if self.user:
            new_tweets = self.api.GetUserTimeline(user_id=self.user.id, count=amount)
            return list(map(lambda e: self._make_text(e), new_tweets))
        else:
            raise TwitterDownloaderException("You have to first set_twitteruser")

    def download_all_tweets(self):
        try:
            alltweets = []
            new_tweets = self.api.GetUserTimeline(user_id=self.user.id, count=200)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
            while len(new_tweets) > 0:
                new_tweets = self.api.GetUserTimeline(user_id=self.user.id, count=200, max_id=oldest)
                alltweets.extend(new_tweets)
                oldest = alltweets[-1].id - 1
        except TwitterError:
            raise TwitterDownloaderException('Error while downloading')
        return list(map(lambda e: self._make_text(e), alltweets))

    @staticmethod
    def _make_text(tweet):
        links = list(map(lambda e: e.expanded_url, tweet.urls))
        hashs = list(map(lambda e: e.text, tweet.hashtags))
        return Text(tweet.text, hashs, links)

    @staticmethod
    def _unshorten_url(url):
        try:
            r = requests.head(url, allow_redirects=True)
            print('Fetching ' + r.url)
            return r.url
        except RequestException:
            raise TwitterDownloaderException('Error appeared while fetching url')


class TwitterDownloaderException(Exception):
    pass