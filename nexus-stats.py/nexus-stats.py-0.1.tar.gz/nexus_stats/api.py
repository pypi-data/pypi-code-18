import requests
from nexus.profile import Profile
from nexus.exceptions import *

class Requester():
    """Represents a connection to the API.
        This class is used to get data from the API and return useful information.
        A few options can be passed to :class:`Requester` to make it easier to use the functions.
        Parameters
        ----------
        max_messages : Optional[int]
            The maximum number of messages to store in :attr:`messages`.
            This defaults to 5000. Passing in `None` or a value less than 100
            will use the default instead of the passed in value.
        loop : Optional[event loop].
            The `event loop`_ to use for asynchronous operations. Defaults to ``None``,
            in which case the default event loop is used via ``asyncio.get_event_loop()``.
        cache_auth : Optional[bool]
            Indicates if :meth:`login` should cache the authentication tokens. Defaults
            to ``True``. The method in which the cache is written is done by writing to
            disk to a temporary directory.
        connector : aiohttp.BaseConnector
            The `connector`_ to use for connection pooling. Useful for proxies, e.g.
            with a `ProxyConnector`_.
        shard_id : Optional[int]
            Integer starting at 0 and less than shard_count.
        shard_count : Optional[int]
            The total number of shards.
        Attributes
        -----------
        user : Optional[:class:`User`]
            Represents the connected client. None if not logged in.
        voice_clients : iterable of :class:`VoiceClient`
            Represents a list of voice connections. To connect to voice use
            :meth:`join_voice_channel`. To query the voice connection state use
            :meth:`is_voice_connected`.
        servers : iterable of :class:`Server`
            The servers that the connected client is a member of.
        private_channels : iterable of :class:`PrivateChannel`
            The private channels that the connected client is participating on.
        messages
            A deque_ of :class:`Message` that the client has received from all
            servers and private messages. The number of messages stored in this
            deque is controlled by the ``max_messages`` parameter.
        email
            The email used to login. This is only set if login is successful,
            otherwise it's None.
        ws
            The websocket gateway the client is currently connected to. Could be None.
        loop
            The `event loop`_ that the client uses for HTTP requests and websocket operations."""
    def __init__(self, **options):
        self.url = "https://api.nexus-stats.com"
        self.userName = options.get("userName", None)

    def get_user_profile(self, userName = None):
        if not userName and not self.userName:
            raise MissingInput("get_user_profile", "userName")

        if not userName:
            userName = self.userName

        response = Profile(self.url, userName)
        return response
