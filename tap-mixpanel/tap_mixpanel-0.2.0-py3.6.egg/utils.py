import json
import os
import urllib
from base64 import b64encode

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def load_schema(entity):
    with open(get_abs_path('schemas/{}.json'.format(entity))) as file:
        return json.load(file)

def authenticate(api_key, session):
    encoded_key = b64encode(bytes("{0}".format(api_key), 'utf-8')).decode("ascii")
    session.headers.update({ 'Authorization': 'Basic {0}'.format(encoded_key)})

def convert_events_to_events_schema(events):
    formatted_events = []
    for event in events['data']['values']:
        formatted_event = {}
        formatted_event['event'] = event
        formatted_event['values'] = {}
        for date in events['data']['values'][event]:
            formatted_event['values'][date] = events['data']['values'][event][date]
        formatted_events.append(formatted_event)
        
    return formatted_events

def build_event_query_param(events_to_get):
    event_query = '['
    for event in events_to_get:
        event_query += '"{0}",'.format(event)
    event_query = event_query[:-1] #strip off last comma
    event_query += "]"
    encoded_event_query = urllib.parse.quote(event_query)
    event_query_param = "&event=" + encoded_event_query

    return event_query_param

def build_date_query_param(state):
    from_date = state['events']['from_date']
    to_date = state['events']['to_date']
    state['events']['from_date'] = to_date
    query_string = '?type=general&unit=day&from_date={0}&to_date={1}'.format(from_date, to_date)

    return query_string

def build_query_string(events_to_get, state):
    if 'events' in state and state['events'] is not None:
        query_string = build_date_query_param(state)
    else:
        query_string = '?type=general&unit=day&interval=7'

    event_query_param = build_event_query_param(events_to_get)
    
    return query_string + event_query_param