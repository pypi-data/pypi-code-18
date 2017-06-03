import enum


class Categories(enum.Enum):
    pass


class Category:
    def __init__(self, *, data):
        self.name = data['name'],
        self.total_channels = data.get('total_channels'),
        self.online_channels = data.get('online_channels'),
        self.viewers = data.get('viewers'),
