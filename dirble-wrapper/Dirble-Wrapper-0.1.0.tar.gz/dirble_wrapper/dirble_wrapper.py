import json
from urllib.request import Request, urlopen

BASE_URL = "http://api.dirble.com/v2/"

# Default parameters
PAGE = 0
PER_PAGE = 20
OFFSET = 0


class ImageThumb(object):
    def __init__(self, **kwargs):
        self.url = kwargs.get("url")


class StationImage(object):
    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        thumb = kwargs.get("thumb")
        self.thumb = ImageThumb(**thumb) if thumb is not None else None


class StationStream(object):
    def __init__(self, **kwargs):
        self.stream = kwargs.get("stream")
        self.bitrate = kwargs.get("bitrate")
        self.content_type = kwargs.get("content_type")
        self.listeners = kwargs.get("listeners")
        self.status = kwargs.get("status")


class Station(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.country = kwargs.get("country")
        self.website = kwargs.get("website")
        image = kwargs.get("image")
        self.image = StationImage(**image) if image is not None else None
        self.slug = kwargs.get("slug")
        streams = kwargs.get("streams")
        self.streams = [StationStream(**s) for s in streams]


class DirbleWrapper(object):

    def __init__(self, token):
        self.token = token

    @staticmethod
    def _handle_request(url):
        return urlopen(url).read().decode("utf-8")

    @staticmethod
    def _handle_stations_post_request(url, data):
        req = Request(url, data=json.dumps(data).encode("utf-8"), headers={'content-type': 'application/json'})
        response = DirbleWrapper._handle_request(req)
        json_response = json.loads(response)
        return [Station(**j) for j in json_response]

    @staticmethod
    def _handle_stations_get_request(url):
        response = DirbleWrapper._handle_request(url)
        json_response = json.loads(response)
        return [Station(**j) for j in json_response]

    def get_all_stations(self, page=PAGE, per_page=PER_PAGE, offset=OFFSET):
        url = "{base}stations?token={t}&page={p}&per_page={pp}&offset={o}".format(
            base=BASE_URL,
            t=self.token,
            p=page,
            pp=per_page,
            o=offset
        )
        return DirbleWrapper._handle_stations_get_request(url)

    def get_recent_added_stations(self, page=PAGE, per_page=PER_PAGE, offset=OFFSET):
        url = "{base}stations/recent?token={t}&page={p}&per_page={pp}&offset={o}".format(
            base=BASE_URL,
            t=self.token,
            p=page,
            pp=per_page,
            o=offset
        )
        return DirbleWrapper._handle_stations_get_request(url)

    def get_popular_stations(self, page=PAGE, per_page=PER_PAGE, offset=OFFSET):
        url = "{base}stations/popular?token={t}&page={p}&per_page={pp}&offset={o}".format(
            base=BASE_URL,
            t=self.token,
            p=page,
            pp=per_page,
            o=offset
        )
        return DirbleWrapper._handle_stations_get_request(url)

    def get_specific_station(self, id):
        url = "{base}stations/{id}?token={t}".format(base=BASE_URL, id=id, t=self.token)
        return DirbleWrapper._handle_stations_get_request(url)

    def search_stations(self, query, page=PAGE, category=None, country=None):
        url = "{base}search?token={t}&page={p}".format(
            base=BASE_URL,
            t=self.token,
            p=page,
        )
        if category is not None:
            url += "&category={c}".format(c=category)
        if country is not None:
            url += "&country={c}".format(c=country)
        return DirbleWrapper._handle_stations_post_request(url, {"query": query})
