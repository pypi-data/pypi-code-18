# -*- coding: utf-8 -*-
import math
from collections import defaultdict
from datetime import datetime
from itertools import groupby

import ephem
import requests
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError
from timezonefinder import TimezoneFinder

tf = TimezoneFinder()


def find_timezone(lat, lng):
    lat = float(lat)
    lng = float(lng)

    try:
        timezone_name = tf.timezone_at(lng=lng, lat=lat)
        if timezone_name is None:
            timezone_name = tf.closest_timezone_at(lng=lng, lat=lat)
            # maybe even increase the search radius when it is still None

    except ValueError:
        # the coordinates were out of bounds
        # {handle error}
        raise
    else:
        print(timezone_name)
        return timezone_name


def localize_dt(utc_datetime, timezone_name):
    try:
        tz = timezone(timezone_name)
        localized_dt = tz.fromutc(utc_datetime)
    except UnknownTimeZoneError:
        # ... handle the error ...
        raise
    else:
        return localized_dt


URL = 'http://iss-positioner.nkoshelev.pro/lst'
# URL = 'http://localhost:8081/lst'

PARAMS = dict(start_dt='2017-06-15',
              end_dt='2017-07-16',
              dist='155',
              units='km',
              min_duration='1')
FILES = dict(lst=open('uragan.lst', 'rb'))


def sun_angle(dt, longitude=None, latitude=None, body=ephem.Sun()):
    obs = ephem.Observer()
    obs.long, obs.lat, obs.date = math.radians(longitude), math.radians(latitude), dt
    body.compute(obs)
    return math.degrees(body.alt)


def main():
    start = datetime.utcnow()
    resp = requests.post(URL, data=PARAMS, files=FILES)
    result = resp.json()
    print(datetime.utcnow() - start)

    if result['error']:
        return

    session = defaultdict(list)
    for title, coords_set in result['data'].items():
        for coords in coords_set:
            session[coords[len(coords)//2]['dt'][:10]].append([dict(title=title, **coord) for coord in coords])

    for dt, coords_set in sorted(session.items(), key=lambda item: item[0]):
        coords_set.sort(key=lambda cs: (cs[0]['dt'], cs[0]['title']))
        print()
        print(dt)
        print('-' * len(dt))
        print('Sun\tstart\tend\tTraverz')
        for coords in coords_set:
            start, traverz, end = coords[0]['dt'], min(coords, key=lambda c: c['dist']), coords[-1]['dt']
            sa = sun_angle(traverz['dt'], **traverz['coord'])
            if 1 < sa < 90:
                print('%s\t%s\t%s\t%s' % (sa, start, end, traverz))


if __name__ == '__main__':
    main()
