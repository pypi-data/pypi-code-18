import requests
from .exceptions import *

class Accolades():
    def __init__(self, data):
        self.founder = data["founder"]
        self.guide = data["guide"]
        self.moderator = data["moderator"]
        self.partner = data["partner"]
        self.staff = data["staff"]

class Rank():
    def __init__(self, data):
        self.name = data["name"]
        self.number = data["number"]
        self.next = data["number"]

class Mastery():
    def __init__(self, data):
        self.rank = Rank(data=data["rank"])
        self.xp = data["xp"]
        self.xpRemaining = data["xpUntilNextRank"]

class Clan():
    def __init__(self, data):
        self.name = data["name"]
        self.rank = data["rank"]
        self.type = data["type"]

class Marked():
    def __init__(self, data):
        self.stalker = data["stalker"]
        self.g3 = data["g3"]
        self.zanuka = data["zanuka"]

class Profile():
    def __init__(self, url, userName):
        self.url = url
        self.ext = "/warframe/v1/players/{}/profile".format(userName)
        self.dataURL = self.url + self.ext

        try:
            response = requests.get(self.dataURL)
            data = response.json()

        except requests.exceptions.MissingSchema:
            raise ServerException("Link not found.")


        try:
            r = data["reason"]
            self.data = False
            if r == "Could not find user in-game.":
                raise UserNotFound()

        except KeyError:
            self.data = True

            if "E: Not Detected" in data:
                # Find field
                pass

            self.name = data["name"]
            self.accolades = Accolades(data=data["accolades"])
            self.mastery = Mastery(data=data["mastery"])
            self.clan = Clan(data=data["clan"])
            self.marked = Marked(data=data["marked"])
            self.createdAt = data["createdAt"]
            self.updatedAt = data["updatedAt"]
