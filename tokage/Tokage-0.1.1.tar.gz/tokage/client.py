from .http import HTTPClient
from .abc import *
from .errors import *

class Client:
    BASE_URL = 'https://jikan.me/api/'
    ANIME_URL = BASE_URL + 'anime/'
    MANGA_URL = BASE_URL + 'manga/'
    PERSON_URL = BASE_URL + 'person/'
    CHARACTER_URL = BASE_URL + 'character/'

    def __init__(self):
        self.client = HTTPClient()

    async def get_anime(self, target_id):
        response_json = await self.client.request(self.ANIME_URL + str(target_id))
        if response_json is None:
            raise AnimeNotFound("Anime with the requested ID was not found")
        result = Anime(target_id, **response_json)
        return result
    async def get_manga(self, target_id):
        response_json = await self.client.request(self.MANGA_URL + str(target_id))
        if response_json is None:
            raise MangaNotFound("Manga with the requested ID was not found")
        result = Manga(target_id, **response_json)
        return result
