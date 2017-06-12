# -*- coding: utf-8 -*-
#
"""
Python library for the Withings API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Withings Body metrics Services API
<http://www.withings.com/en/api/wbsapiv2>

Uses Oauth 1.0 to authentify. You need to obtain a consumer key
and consumer secret from Withings by creating an application
here: <https://oauth.withings.com/partner/add>

Usage:

auth = WithingsAuth(CONSUMER_KEY, CONSUMER_SECRET)
authorize_url = auth.get_authorize_url()
print "Go to %s allow the app and copy your oauth_verifier" % authorize_url
oauth_verifier = raw_input('Please enter your oauth_verifier: ')
creds = auth.get_credentials(oauth_verifier)

client = WithingsApi(creds)
measures = client.get_measures(limit=1)
print "Your last measured weight: %skg" % measures[0].weight

"""

from __future__ import unicode_literals

import pytz

__title__ = 'withings'
__version__ = '0.1'
__author__ = 'Maxime Bouroumeau-Fuseau'
__license__ = 'MIT'
__copyright__ = 'Copyright 2012 Maxime Bouroumeau-Fuseau'

__all__ = [str('WithingsCredentials'), str('WithingsAuth'), str('WithingsApi'),
           str('WithingsMeasures'), str('WithingsMeasureGroup')]

import requests
from requests_oauthlib import OAuth1, OAuth1Session
import json
import datetime

# Workout categories
WORKOUT_WALK = 1
WORKOUT_RUN = 2
WORKOUT_HIKING = 3
WORKOUT_STAKING = 4
WORKOUT_BMX = 5
WORKOUT_BICYCLING = 6
WORKOUT_SWIM = 7
WORKOUT_SURFING = 8
WORKOUT_KITESURFING = 9
WORKOUT_WINDSURFING = 10
WORKOUT_BODYBOARD = 11
WORKOUT_TENNIS = 12
WORKOUT_TABLE_TENNIS = 13
WORKOUT_QUASH = 14
WORKOUT_BADMINTON = 15
WORKOUT_LIFT_WEIGHTS = 16
WORKOUT_CALISTHENICS = 17
WORKOUT_ELLIPTICAL = 18
WORKOUT_ILATE = 19
WORKOUT_BASKETBALL = 20
WORKOUT_SOCCER = 21
WORKOUT_FOOTBALL = 22
WORKOUT_RUGBY = 23
WORKOUT_VOLLYBALL = 24
WORKOUT_WATERPOLO = 25
WORKOUT_HORSERIDING = 26
WORKOUT_GOLF = 27
WORKOUT_YOGA = 28
WORKOUT_DANCING = 29
WORKOUT_BOXING = 30
WORKOUT_FENCING = 31
WORKOUT_WRESTLING = 32
WORKOUT_MARTIAL_ARTS = 33
WORKOUT_SKIING = 34
WORKOUT_SNOWBOARDING = 35
WORKOUT_HANDBALL = 192
WORKOUT_DANCING2 = 29
WORKOUT_BASE = 186
WORKOUT_ROWING = 187
WORKOUT_ZUMBA = 188
WORKOUT_BASEBALL = 191
WORKOUT_HANDBALL2 = 192
WORKOUT_HOCKEY = 193
WORKOUT_ICEHOCKEY = 194
WORKOUT_CLIMBING = 195
WORKOUT_ICESKATING = 196

# The measuregroup has been captured by a device and is known to belong to this user (and is not ambiguous)
ATTRIB_CAPTURED_BY_DEVICE_NOT_AMBIGUOUS = 0
# The measuregroup has been captured by a device but may belong to other users as well as this one (it is ambiguous)
ATTRIB_CAPTURED_BY_DEVICE_AMBIGUOUS = 1
# The measuregroup has been entered manually for this particular user
ATTRIB_ENTERED_MANUALLY = 2
#  The measuregroup has been entered manually during user creation (and may not be accurate)r
ATTRIB_ENTERED_MANUALLY_INACCURATE = 4
# Measure auto, it's only for the Blood Pressure Monitor. This device can make many measures and computed the best value
ATTRIB_MEASURE_AUTO = 5
# Measure confirmed. You can get this value if the user confirmed a detected activity
ATTRIB_DETECTED_CONFIRMED = 7


class WithingsCredentials(object):
    def __init__(self, access_token=None, access_token_secret=None,
                 consumer_key=None, consumer_secret=None, user_id=None):
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.user_id = user_id


class WithingsError(Exception):
    STATUS_CODES = {
        # Response status codes as defined in documentation
        # http://oauth.withings.com/api/doc
        0: u"Operation was successful",
        247: u"The userid provided is absent, or incorrect",
        250: u"The provided userid and/or Oauth credentials do not match",
        286: u"No such subscription was found",
        293: u"The callback URL is either absent or incorrect",
        294: u"No such subscription could be deleted",
        304: u"The comment is either absent or incorrect",
        305: u"Too many notifications are already set",
        342: u"The signature (using Oauth) is invalid",
        343: u"Wrong Notification Callback Url don't exist",
        601: u"Too Many Request",
        2554: u"Wrong action or wrong webservice",
        2555: u"An unknown error occurred",
        2556: u"Service is not defined",
    }

    def __init__(self, status):
        super(WithingsError, self).__init__(u'{}: {}'.format(status, WithingsError.STATUS_CODES[status]))
        self.status = status


class WithingsAuth(object):
    URL = 'https://oauth.withings.com/account'

    def __init__(self, consumer_key, consumer_secret, callback_uri=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = None
        self.oauth_secret = None
        self.callback_uri=callback_uri

    def get_authorize_url(self):
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret,
                              callback_uri=self.callback_uri)

        tokens = oauth.fetch_request_token('%s/request_token' % self.URL)
        self.oauth_token = tokens['oauth_token']
        self.oauth_secret = tokens['oauth_token_secret']

        return oauth.authorization_url('%s/authorize' % self.URL)

    def get_credentials(self, oauth_verifier):
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret,
                              resource_owner_key=self.oauth_token,
                              resource_owner_secret=self.oauth_secret,
                              verifier=oauth_verifier)
        tokens = oauth.fetch_access_token('%s/access_token' % self.URL)
        return WithingsCredentials(access_token=tokens['oauth_token'],
                                   access_token_secret=tokens['oauth_token_secret'],
                                   consumer_key=self.consumer_key,
                                   consumer_secret=self.consumer_secret,
                                   user_id=tokens['userid'])


class WithingsApi(object):
    URL = 'http://wbsapi.withings.net'
    URL_V2 = URL + '/v2'

    def __init__(self, credentials):
        self.credentials = credentials
        self.oauth = OAuth1(credentials.consumer_key,
                            credentials.consumer_secret,
                            credentials.access_token,
                            credentials.access_token_secret,
                            signature_type='query')
        self.client = requests.Session()
        self.client.auth = self.oauth
        self.client.params.update({'userid': credentials.user_id})

    def request(self, service, action, params=None, method='GET', url=URL):
        if params is None:
            params = {}
        params['action'] = action
        r = self.client.request(method, '%s/%s' % (url, service), params=params)
        response = json.loads(r.content.decode())
        if response['status'] != 0:
            raise WithingsError(response['status'])
        return response.get('body', None)

    def get_user(self):
        return self.request('user', 'getbyuserid')

    def get_measures(self, **kwargs):
        r = self.request('measure', 'getmeas', kwargs)
        return WithingsMeasures(r)

    def get_workouts(self, **kwargs):
        def fetch(offset=None):
            if offset is not None:
                kwargs.update({
                    'offset': offset,
                })
            return self.request('measure', 'getworkouts', params=kwargs, url=self.URL_V2)
        data = fetch()
        return Workouts(data, fetch)

    def subscribe(self, callback_url, comment, appli=1):
        params = {'callbackurl': callback_url,
                  'comment': comment,
                  'appli': appli}
        self.request('notify', 'subscribe', params)

    def unsubscribe(self, callback_url, appli=1):
        params = {'callbackurl': callback_url, 'appli': appli}
        self.request('notify', 'revoke', params)

    def is_subscribed(self, callback_url, appli=1):
        params = {'callbackurl': callback_url, 'appli': appli}
        try:
            self.request('notify', 'get', params)
            return True
        except:
            return False

    def list_subscriptions(self, appli=1):
        r = self.request('notify', 'list', {'appli': appli})
        return r['profiles']


class WithingsMeasures(list):
    def __init__(self, data):
        super(WithingsMeasures, self).__init__([WithingsMeasureGroup(g) for g in data['measuregrps']])
        self.updatetime = datetime.datetime.fromtimestamp(data['updatetime'])


class WithingsMeasureGroup(object):
    MEASURE_TYPES = (('weight', 1), ('height', 4), ('fat_free_mass', 5),
                     ('fat_ratio', 6), ('fat_mass_weight', 8),
                     ('diastolic_blood_pressure', 9), ('systolic_blood_pressure', 10),
                     ('heart_pulse', 11))

    def __init__(self, data):
        self.data = data
        self.grpid = data['grpid']
        self.attrib = data['attrib']
        self.category = data['category']
        self.date = datetime.datetime.fromtimestamp(data['date'])
        self.measures = data['measures']
        for n, t in self.MEASURE_TYPES:
            self.__setattr__(n, self.get_measure(t))

    def is_ambiguous(self):
        return self.attrib in (ATTRIB_CAPTURED_BY_DEVICE_AMBIGUOUS, ATTRIB_ENTERED_MANUALLY_INACCURATE)

    def is_measure(self):
        return self.category == ATTRIB_CAPTURED_BY_DEVICE_AMBIGUOUS

    def is_target(self):
        return self.category == ATTRIB_ENTERED_MANUALLY

    def get_measure(self, measure_type):
        for m in self.measures:
            if m['type'] == measure_type:
                return m['value'] * pow(10, m['unit'])
        return None


class Workout(object):
    attrib = None
    category = None
    date = None
    enddate = None
    id = None
    model = None
    modified = None
    startdate = None
    timezone = None
    userid = None
    data = None

    def __init__(self, data):
        super(Workout, self).__init__()
        # Parse data to Python values
        data['date'] = datetime.datetime.strptime(data['date'], '%Y-%m-%d').date()
        data['timezone'] = pytz.timezone(data['timezone'])
        for field in 'enddate', 'modified', 'startdate':
            data[field] = datetime.datetime.fromtimestamp(data[field], tz=data['timezone'])

        # Assign to fields
        for k, v in data.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)


class Workouts(object):
    """
    Workout iterator
    Lazily fetches workout data and yields Workout objects
    """
    def __init__(self, data, fetch_page):
        super(Workouts, self).__init__()
        self.data = data
        self.fetch_page = fetch_page

    def __iter__(self):
        data = self.data
        while True:
            for activity in data['series']:
                yield Workout(activity)
            if not data['more']:
                break
            data = self.fetch_page(data['offset'])
