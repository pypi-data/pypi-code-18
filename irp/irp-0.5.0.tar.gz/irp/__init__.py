import os
import requests
import logging

from functools import lru_cache


IATACODES_API_KEY = os.environ.get('IATACODES_API_KEY')


@lru_cache(None)
def cached_json_get(url):
    """
    Makes a get to that URL and caches it. Simple right? Oh it also returns the
    JSON as a dict for you already!
    """
    return requests.get(url).json()


try:
    CITIES = requests.get("https://iatacodes.org/api/v6/cities?api_key={}".format(
        IATACODES_API_KEY
    ), verify=False).json()['response']

    AIRPORTS = requests.get(
        "https://iatacodes.org/api/v6/airports?api_key={}".format(
            IATACODES_API_KEY
        ),
        verify=False,
    ).json()['response']

    COUNTRIES = requests.get(
        "https://restcountries.eu/rest/v2/all"
    ).json()
except Exception as exc:
    logging.exception('Failed to get data for IRP!')


def get_airports(str_city):
    """
    Returns all airport codes of available cities that match the users
    location with their country code.

    :param str_city: The user input.
    :return:         Yields tuples with the airport code and the country code.
    """
    str_city = str_city.lower().strip()

    if ',' in str_city:
        city_part, country_part = map(str.strip, str_city.split(','))
    else:
        city_part, country_part = str_city, None

    if len(city_part) == 3:
        try:
            yield city_part.upper(), [city['country_code']
                                      for city in CITIES
                                      if city['code'].lower() == city_part][0]
            return
        except IndexError:
            pass  # No airport with that code available! Go on.

    for city in CITIES:
        if (city['name'].lower() == city_part and
                (not country_part or
                 country_part == city['country_code'].lower())):
            yield city['code'], city['country_code']


def get_airport(airport: str):
    """
    :param airport: A three letter code, e.g. IRP
    """
    uppered = airport.upper()
    for airport in AIRPORTS:
        if airport['code'] == uppered:
            return airport


def get_name(airport: str):
    """
    :param airport: A three letter code, e.g. IRP
    """
    uppered = airport.upper()
    for city in CITIES:
        if city['code'] == uppered:
            return city['name']

    airport = get_airport(airport)
    if airport:
        return airport['name']


def get_airport_country(airport: str):

    ADDR_INFO = "https://maps.googleapis.com/maps/api/geocode/json?address={0}%20Airport&sensor=false"
    airport_info = cached_json_get(ADDR_INFO.format(airport))

    comps = airport_info['results'][0]['address_components']
    for comp in comps:
        if 'country' in comp['types']:
            return comp['long_name'], comp['short_name']

def get_currency(airport: str):
    """
    :param airport: A three letter airport code
    """
    country, short = get_airport_country(airport)
    for _country in COUNTRIES:
        if short == _country['alpha2Code']:
            return _country['currencies']
