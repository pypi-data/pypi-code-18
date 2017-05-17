import argparse
import requests
import singer
import json

from tap_mixpanel import utils

base_url = 'https://mixpanel.com/api/2.0/'
endpoints = {
    "events" : "events"
}
session = requests.Session()
logger = singer.get_logger()

def http_get(url):
    resp = session.request(method='get', url=url)
    return resp

def get_all_events(events_to_get, state):
    query_string = utils.build_query_string(events_to_get, state)
    response = http_get(base_url + endpoints['events'] + query_string)
    events = response.json()

    formatted_events = utils.convert_events_to_events_schema(events)
    singer.write_records('events', formatted_events)
    
    return state

def sync_events(events_to_get, state):
    event_schema = utils.load_schema('events')
    singer.write_schema('events', event_schema, 'legend_size')
    state = get_all_events(events_to_get, state)
    singer.write_state(state)

def do_sync(config, state):
    logger.info("Starting Mixpanel sync")
    api_key = config['api-secret']
    events_to_get = config['event-names']
    utils.authenticate(api_key, session)

    if state:
        logger.info('Replicating events from {0} to {1}'.format(state['events']['from_date'], state['events']['to_date']))
    else:
        logger.info('Replicating all events from the past 7 days')

    sync_events(events_to_get, state)

    logger.info("Done Mixpanel sync")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config', help='Config file', required=True)
    parser.add_argument(
        '-s', '--state', help='State file')

    args = parser.parse_args()
    with open(args.config) as config_file:
        config = json.load(config_file)

    missing_keys = []
    for key in ['api-secret', 'event-names']:
        if key not in config:
            missing_keys += [key]

    if len(missing_keys) > 0:
        logger.fatal("Missing required configuration keys: {}".format(missing_keys))
        exit(1)

    events_to_get = config['event-names']
    if not events_to_get:
        logger.fatal("No events specified in config.json")
        exit(1)

    state = {}
    if args.state:
        with open(args.state, 'r') as data_file:
            state = json.load(data_file)

    do_sync(config, state)
    
if __name__ == '__main__':
    main()
