import requests
import json
from .models import *

class ApiObject:
    def __init__(self, api_key):
        """Initiate a TBA ApiObject

        Positional arguments:
        api_key -- API key from TBA (found at https://www.thebluealliance.com/account)
        """
        if not api_key:
            raise Exception('API Key not provided')
        self.header = {'X-TBA-Auth-Key': api_key, 'accept': 'json'}
        self.base = 'https://www.thebluealliance.com/api/v3/'
        s = self.status()
        if s.is_datafeed_down:
            print(s.is_datafeed_down)
            raise Exception('TBA Datafeed is currently down')
        self.max_season = s.max_season
        self.current_season = s.current_season

    def status(self):
        """Gets status of ApiObbject"""
        r = self.make_request('status')
        return Status(r)

    def teams_page(self, page_number):
        """Returns a list of team objects on a page

        Positional arguments:
        page_number -- page number to search for (zero-indexed)

        Note: calls team_page_year with current year
        """
        return self.teams_page_year(page_number)

    def teams_page_simple(self, page_number):
        """Returns a list of team objects on a page, reported with limited information

        Positional arguments:
        page_number -- page number to search for (zero-indexed)

        Note: Calls team_page_year_simple with current year
        Note: Creates Team object with only key, team number, nick, name, city, state, and country
        """
        return self.teams_page_year_simple(page_number)

    def teams_page_keys(self, page_number):
        """Returns a list of team keys on a page

        Positional arguments:
        page_number -- page number to search for (zero-indexed)

        Note: Calls team_page_year_keys with current year
        """
        return self.teams_page_year_keys(page_number)

    def teams_page_year(self, page_number, year=None):
        """Returns a list of team objects on a page that competed in a specified year

        Positional arguments:
        page_number -- page number to search for (zero-indexed)

        Keyword arguments:
        year -- year to find participating teams. Defaults to current year
        """
        if not year:
            year = self.current_season
        if year > self.max_season:
            raise Exception('Year requested is in the future.')
        r = self.make_request('teams/' + str(year) + '/' + str(page_number)).json()
        return [Team(t) for t in r]

    def teams_page_year_simple(self, page_number, year=None):
        """Returns a list of team objects on a page that competed in a specified year, reported with limited information

        Positional arguments:
        page_number -- page number to search for (zero-indexed)

        Keyword arguments:
        year -- year to find participating teams. Defaults to current year
        """
        if not year:
            year = self.current_season
        if year > self.max_season:
            raise Exception('Year requested is in the future.')
        r = self.make_request('teams/' + str(year) + '/' + str(page_number) + '/simple').json()
        return [Team(t) for t in r]

    def teams_page_year_keys(self, page_number, year=None):
        """Returns a list of team keys on a page that competed in a specified year

        Positional arguments:
        page_number -- page number to search for (zero-indexed)

        Keyword arguments:
        year -- year to find participating teams. Defaults to current year
        """
        if not year:
            year = self.current_season
        if year > self.max_season:
            raise Exception('Year requested is in the future.')
        r = self.make_request('teams/' + str(year) + '/' + str(page_number) + '/keys').json()
        return [k for k in r]

    def get_team(self, key):
        """Returns a team object

        Positional arguments:
        key -- key of specified team
        """
        r = self.make_request('team/' + str(key))
        return Team(r)

    def get_team_simple(self, key):
        """Returns a team object, reported with limited information

        Positional arguments:
        key -- key of specified team
        """
        r = self.make_request('team/' + str(key) + '/simple')
        return Team(r)

    def years_participated(self, key):
        """Returns a list of years a team has competed

        Positional arguments:
        key -- key of specified team
        """
        r = self.make_request('team/' + str(key) + '/years_participated').json()
        return r

    def team_districts(self, key):
        """Returns a list of district objects for each year a team has participated in the district system

        Positional arguments:
        key -- key of specified team
        """
        r = self.make_request('team/' + str(key) + '/districts').json()
        return [District(d) for d in r]

    def team_robots(self, key):
        """Returns a list of a team's robots

        Positional arguments:
        key -- key of specified team
        """
        r = self.make_request('team/' + str(key) + '/robots').json()
        return [Robot(robo) for robo in r]

    def team_events(self, key):
        """Returns list of events a team has competed at

        Positional arguments:
        key -- key of specified team
        """
        r = self.make_request('team/' + str(key) + '/events').json()
        return [Event(e) for e in r]

    def team_events_simple(self, key):
        """Returns list of events a team has competed at, reported with limited information

        Positional arguments:
        key -- key of specified team
        """
        r = self.make_request('team/' + str(key) + '/events/simple').json()
        return [Event(e) for e in r]

    def team_events_keys(self, key):
        """Returns a list of event keys for a team

        Positional arguments:
        key -- key of specified item
        """
        r = self.make_request('team/' + str(key) + '/events/keys').json()
        return [k for k in r]

    def team_events_year(self, key, year=None):
        """Returns a list of events competed in by a team in a given year

        Positional arguments:
        key -- key of specified team

        Keyword arguments:
        year -- year to search for events. Defaults to current year
        """
        if not year:
            year = self.current_season
        r = self.make_request('team/' + str(key) + '/events/' + str(year)).json()
        return [Event(e) for e in r]

    def team_events_year_simple(self, key, year=None):
        """Returns a list of events competed in by a team in a given year, reported with limited information

        Positional arguments:
        key -- key of specified team

        Keyword arguments:
        year -- year to search for events. Defaults to current year
        """
        if not year:
            year = self.current_season
        r = self.make_request('team/' + str(key) + '/events/' + str(year) + '/simple').json()
        return [Event(e) for e in r]

    def team_events_year_keys(self, key, year=None):
        """Returns a list of event keys for a team in a given year

        Positional arguments:
        key -- key of specified team

        Keyword arguments:
        year -- year to find events. Defaults to current year
        """
        if not year:
            year = self.current_season
        r = self.make_request('team/' + str(key) + '/events/' + str(year) + '/keys').json()
        return [k for k in r]

    def team_event_matches(self, team_key, event_key):
        """Returns a list of Match objects for a team at an event

        Positional arguments:
        team_key -- key of specified team
        event_key -- key of specified event
        """
        r = self.make_request('team/' + str(team_key) + '/event/' + str(event_key) + '/matches').json()
        return [Match(m) for m in r]

    def team_event_matches_simple(self, team_key, event_key):
        """Returns a list of Match objects for a team at an event, reported with limited information

        Positional arguments:
        team_key -- key of specified team
        event_key -- key of specified event
        """
        r = self.make_request('team/' + str(team_key) + '/event/' + str(event_key) + '/matches/simple').json()
        return [Match(m) for m in r]

    def team_event_matches_keys(self, team_key, event_key):
        """Returns a list of keys for matches for a team at an event

        Positional arguments:
        team_key -- key of specified team
        event_key -- key of specified event
        """
        r = self.make_request('team/' + str(team_key) + '/event/' + str(event_key) + '/matches/keys').json()
        return [k for k in r]

    def team_event_status(self, team_key, event_key):
        """Returns an EventStatus object correlating to a team at an event

        Positional arguments:
        team_key -- key of specified team
        event_key -- key of specified event
        """
        r = self.make_request('team/' + str(team_key) + '/event/' + str(event_key) + '/status')
        return EventStatus(r)

    def team_awards(self, team_key):
        """Returns a list of awards a team has won

        Positional arguments:
        team_key -- key of specified team
        """
        r = self.make_request('team/' + str(team_key) + '/awards').json()
        return [Award(a) for a in r]

    def team_awards_year(self, team_key, year=None):
        """Returns a list of awards a team has won in a given year

        Positional arguments:
        team_key -- key of specified team

        Keyword arguments:
        year -- year to search for awards in. Defaults to current year
        """
        if not year:
            year = self.current_season
        r = self.make_request('team/' + str(team_key) + '/awards/' + str(year)).json()
        return [Award(a) for a in r]

    def team_matches_year(self, team_key, year=None):
        """Returns a list of matches compteted in a year by a team

        Positional arguments:
        team_key -- key of specified team

        Keyword arguments:
        year -- year to search for matches. Defaults to current year
        """
        if not year:
            year = self.current_season
        r = self.make_request('team/' + str(team_key) + '/matches/' + str(year)).json()
        return [Match(m) for m in r]

    def team_matches_year_simple(self, team_key, year=None):
        """Returns a list of matches compteted in a year by a team, reported with limited information

        Positional arguments:
        team_key -- key of specified team

        Keyword arguments:
        year -- year to search for matches. Defaults to current year
        """
        if not year:
            year = self.current_season
        r = self.make_request('team/' + str(team_key) + '/matches/' + str(year) + '/simple').json()
        return [Match(m) for m in r]

    def team_matches_year_keys(self, team_key, year=None):
        """Returns a list of match keys competed in a year by a team

        Positional arguments:
        team_key -- key of specified team

        Keyword arguments:
        year -- year to search for matches. Defaults to current year
        """
        if not year:
            year = self.current_season
        r = self.make_request('team/' + str(team_key) + '/matches/' + str(year) + '/keys').json()
        return [k for k in r]

    def team_media_year(self, team_key, year=None):
        """Returns a list of media for a team in a given year

        Positional argumnets:
        team_key -- key of specified team

        Keyword arguments:
        year -- year to search for media. Defaults to current year
        """
        if not year:
            year = self.current_season
        r = self.make_request('team/' + str(team_key) + '/media/' + str(year)).json()
        return [Media(m) for m in r]

    def team_social_media(self, team_key):
        """Returns a list of a team's social media

        Positional arguments:
        team_key -- key of specified team
        """
        r = self.make_request('team/' + str(team_key) + '/social_media').json()
        return [Media(m) for m in r]

    def event_teams(self, event_key):
        """Returns a list of teams at a given event

        Positional arguments:
        event_key -- key of event
        """
        r = self.make_request('event/' + str(event_key) + '/teams').json()
        return [Team(t) for t in r]

    def event_teams_simple(self, event_key):
        """Returns a list of teams at a given event, reported with limited information

        Positional arguments:
        event_key -- key of event
        """
        r = self.make_request('event/' + str(event_key) + '/teams/simple').json()
        return [Team(t) for t in r]

    def event_teams_keys(self, event_key):
        """Returns a list of team keys at a given event

        Positional arguments:
        event_key -- key of specified event
        """
        r = self.make_request('event/' + str(event_key) + '/teams/keys').json()
        return [k for k in r]

    def district_teams(self, district_key):
        """Returns a list of teams belonging to a given district

        Positional arguments:
        district_key -- key of specified district
        """
        r = self.make_request('district/' + str(district_key) + '/teams').json()
        return [Team(t) for t in r]

    def district_teams_simple(self, district_key):
        """Returns a list of teams belonging to a given district, reported with limited information

        Positional arguments:
        district_key -- key of specified district
        """
        r = self.make_request('district/' + str(district_key) + '/teams/simple').json()
        return [Team(t) for t in r]

    def district_teams_keys(self, event_key):
        """Returns a list of team keys belonging to a given district

        Positional arguments:
        district_key -- key of specified district
        """
        r = self.make_request('district/' + str(district_key) + '/teams/keys').json()
        return [k for k in r]

    def make_request(self, url):
        """Helper function to make request to TBA"""
        r = requests.get(self.base + url, headers = self.header)
        if r.status_code == 200:
            return r
        if r.status_code == 401:
            raise Exception('Not Authorized - No TBA v3 API Key was provided, or it is not valid.')
        raise Exception('Could not connect to TBA API -- Status code ' + str(r.status_code))


