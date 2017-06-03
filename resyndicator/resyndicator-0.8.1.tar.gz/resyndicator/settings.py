TIMEOUT = 10  # For requests
FETCHER_SLEEP = 10  # For feed/sitemap/etc. fetchers
CONTENT_FETCHER_SLEEP = 5
DEFAULT_LENGTH = 30
INCLUDE_SOURCE = False
TWITTER_STREAM_GET_INTERVAL = 50  # Every n tweets
HUB = 'http://pubsubhubbub.appspot.com/'
TWITTER_TITLE_LENGTH = 80
BASE_COMMANDS = {
    'fetchers': 'resyndicator.services.fetchers',
    'content': 'resyndicator.services.content',
    'stream': 'resyndicator.services.stream',
    'random_urn': 'resyndicator.utils.random_urn',
    'shell': 'resyndicator.utils.ipython',
    'sheck': 'resyndicator.utils.ipython',  # Alias for the faint of heart
}
COMMANDS = {}
USER_AGENT = 'Mozilla/5.0 (compatible; resyndicator)'
WEBROOT = 'webroot/'
DATABASE = 'sqlite://'
BASE_URL = None
ENTRY_CLASS = None
RESOURCES = 'resyndicator'
UNIQUE_LINKS = False  # Use not only ID but also links to make articles unique
