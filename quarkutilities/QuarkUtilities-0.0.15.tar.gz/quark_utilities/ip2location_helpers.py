# coding=utf8
from asyncio import futures

import functools
import geoip2.database
import concurrent.futures
from tornado import gen
import os
current_dir = os.path.dirname(os.path.realpath(__file__))

# This creates a Reader object. You should use the same object
# across multiple requests as creation of it is expensive.
reader = geoip2.database.Reader(
    os.path.join(
        current_dir,
        '../',
        'app_data/GeoIP2-City.mmdb'
    )
)

executor = concurrent.futures.ThreadPoolExecutor(2)


async def get_location(ip_address):
    '''
    Ip adresinin ülkesini getirmek için
    '''
    response = await futures.wrap_future(executor.submit(
        functools.partial(reader.city, ip_address)
    ))

    if not response:
        return None

    return {
        'country': response.country.name,
        'city': response.city.name,
        'latitude': response.location.latitude,
        'longitude': response.location.longitude
    }
