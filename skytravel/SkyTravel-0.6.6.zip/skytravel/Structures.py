import xml.etree.ElementTree as ET
import urllib.request as ur

class Flight(object):
    """
    Class that represents flight
    """
    def __init__(self, price, currency, people,  link, agent, leg):
        """
        Create object of class Flight
        :param price: price of tickets
        :param currency: currency
        :param people: 
        :param link: link for reservating tickets
        :param agent: object that represents travel agent
        :param leg: object that represents leg
        """
        self.price = price*people
        self.currency = currency
        self.link = link
        self.agent = agent
        self.leg = leg

    def agent_info(self):
        """
        Return information about travel agent
        """
        return "Agent #{} - {}".format(self.agent.id, self.agent.name)

    def leg_info(self):
        """
        Return information about leg
        """
        return "Flight #{} from {} to {}".format(self.leg.number, self.leg.origin(), self.leg.destination())

    def __str__(self):
        """
        Return information about flight
        """
        line = self.leg_info()
        line += ' costs {} {}'.format(self.price, self.currency)
        return line


class Agent(object):
    """
    Class that represents travel agent
    """
    def __init__(self, id, name, url):
        """
        Create object of Agent class
        :param id: agent id
        :param name: agent name
        :param url: url to icon of agent
        """
        self.id = id
        self.name = name
        self.url = url


class Agents(object):
    """
    Class that represents all travel agents
    """
    def __init__(self, agents):
        """
        Create object of Agents class of list of Agents
        :param agents: all agents
        """
        self.agents = agents
    
    def by_id(self, id):
        """
        Return certain agent by his id
        :param id: agent id
        :return: Agent object
        """
        for agent in self.agents:
            if agent.id == id:
                return agent

class Leg(object):
    """
    Class that represents leg
    """
    def __init__(self, id, number, origin_stat, destin_stat, places):
        """
        Create object of Leg class
        :param id: leg id
        :param number: leg number
        :param origin_stat: id of origin station
        :param destin_stat: id of destination station
        :param places: all Places
        """
        self.id = id
        self.number = number
        self.origin_stat = origin_stat
        self.destin_stat = destin_stat
        self.places = places

    def origin(self):
        """
        Return Place that is origin station
        """
        return self.places.city_name(self.origin_stat)

    def destination(self):
        """
        Return Place that is destination station
        """
        return self.places.city_name(self.destin_stat)


class Legs(object):
    """
    Class that represents all legs
    """
    def __init__(self, legs):
        """
        Create object of Legs class of list of les
        :param agents: all legs
        """
        self.legs = legs
    
    def by_id(self, id):
        """
        Return certain leg by its id
        :param id: leg id
        :return: Leg object
        """
        for leg in self.legs:
            if leg.id == id:
                return leg


class Place(object):
    """
    Class that represents place
    """
    def __init__(self, id, code, parentid=0):
        """
        Create object of Place class
        :param id: place id
        :param code: code
        :param parentid: id of place that is higher in hierarchy or 0 if it's the highest
        """
        self.id = id
        self.parentid = parentid
        self.code = code
        self.name = None


class Places(object):
    """
    Class that represents all places
    """
    def __init__(self, places, key):
        """
        Create object of Places class of list of places
        :param places: all places
        :param key: api_key
        """
        self.places = places
        self.__key = key

    def by_id(self, id):
        """
        Return certain place by its id
        :param id: leg id
        :return: Leg object
        """
        for place in self.places:
            if place.id == id:
                return place

    def city_name(self, id):
        """
        Return city name by its id
        :param id: city id
        :return: Code of city
        """
        airport = self.by_id(id)
        city = None
        for city in self.places:
            if city.id == airport.parentid:
                break
        for country in self.places:
            if country.id == city.parentid:
                break
        url = 'http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/RU/GBP/en?id='+airport.code+'-sky&apiKey='+self.__key
        r = eval(ur.urlopen(url).read().decode('utf8'))
        return r['Places'][0]['PlaceName']