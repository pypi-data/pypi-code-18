from .category import Category


class Channel:
    def __init__(self, *, data):
        self.user_id = data['user_id']
        self.name = data['name']
        self.viewers = data['viewers']
        self.category = Category(data={'name': data['category']})
        self.adult = data['adult']
        self.gaming = data['gaming']
        self.multistream = data['multistream']
        self.online = data.get('online')
        self.viewers_total = data.get('viewers_total')
        self.followers = data.get('followers')
        self.account_type = data.get('account_type')
        self.commissions = data.get('commissions')
        self.title = data.get('title')
        self.description = data.get('description')
        self.private = data.get('private')
        self.guest_chat = data.get('guest_chat')
        self.last_live = data.get('last_live')
        self.tags = data.get('tags')

    @property
    def avatar_url(self):
        return f'https://picarto.tv/user_data/usrimg/{self.name.lower()}/dsdefault.jpg'

    @property
    def thumbnail_url(self):
        return f'https://thumb.picarto.tv/thumbnail/{self.name.lower()}.jpg'


class OnlineChannel(Channel):
    def __init__(self, *, data):
        super().__init__(data=data)
