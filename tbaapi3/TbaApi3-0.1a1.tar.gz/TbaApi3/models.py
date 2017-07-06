import requests
import datetime

class Util:
    @staticmethod
    def parse(response):
        """Parses and returns a JSON Response, checking for validity"""
        if isinstance(response, dict):
            json = response
        else:
            json = response.json()

        if json.get('Error'):
            raise Exception('Error in retrieval: ' + self.json['error'])

        return json

    @staticmethod
    def pformat(class_instance):
        """'Pretty' formats a class to be printed"""
        s = ''
        for var, val in vars(class_instance).items():
            s += var + ': ' + str(val) + '\n'
        return s[:-1]

class Status:
    def __init__(self, response):
        self.json = Util.parse(response)

        self.current_season = self.json['current_season']
        self.max_season = self.json['max_season']
        self.is_datafeed_down= self.json['is_datafeed_down']
        self.down_events = self.json['down_events']
        self.ios_json = self.json['ios']
        self.android_json = self.json['android']

    def __str__(self):
        return Util.pformat(self)

class Team:
    def __init__(self, response):
        self.json = Util.parse(response)

        # Data that should be found in simple or verbose form
        self.key = self.json['key']
        self.team_number = self.json['team_number']
        self.nickname = self.json['nickname']
        self.name = self.json['name']
        self.city = self.json['city']
        self.state_prov = self.json['state_prov']
        self.country = self.json['country']

        # Data not found in simple form
        try:
            self.address = self.json['address']
            self.postal_code = self.json['postal_code']
            self.gmaps_place_id = self.json['gmaps_place_id']
            self.gmaps_url = self.json['gmaps_url']
            self.lat = self.json['lat']
            self.lng = self.json['lng']
            self.location_name = self.json['location_name']
            self.website = self.json['website']
            self.rookie_year = self.json['rookie_year']
            self.motto = self.json['motto']
            self.home_championship = self.json['home_championship']
        except KeyError:
            self.address = None
            self.postal_code = None
            self.gmaps_place_id = None
            self.gmaps_url = None
            self.lat = None
            self.lng = None
            self.location_name = None
            self.website = None
            self.rookie_year = None
            self.motto = None
            self.home_championship = None

        # Calculated attributes for user convenience
        if self.rookie_year:
            self.years_as_team = datetime.date.today().year - self.rookie_year
        else:
            self.years_as_team = None

    def __str__(self):
        return Util.pformat(self)

class Event:
    def __init__(self,response):
        self.json = Util.parse(response)

        # Data that should be contained in simple or verbose form
        self.key = self.json['key']
        self.name = self.json['name']
        self.event_code = self.json['event_code']
        self.event_type = self.json['event_type']
        self.district_json = self.json['district']
        self.year = self.json['year']
        self.state_prov = self.json['state_prov']
        self.city = self.json['city']
        self.start_date = self.json['start_date']
        self.country = self.json['country']

        # Data not found in simple form
        try:
            self.webcasts_json = self.webcasts = self.json['webcasts']
            self.postal_code = self.json['postal_code']
            self.playoff_type = self.json['playoff_type']
            self.week = self.json['week']
            self.timezone = self.json['timezone']
            self.first_event_id = self.json['first_event_id']
            self.gmaps_place_id = self.json['gmaps_place_id']
            self.short_name = self.json['short_name']
            self.end_date = self.json['end_date']
            self.gmaps_url = self.json['gmaps_url']
            self.address = self.json['address']
            self.lng = self.json['lng']
            self.website = self.json['website']
            self.event_type_string = self.json['event_type_string']
            self.parent_event_key = self.json['parent_event_key']
            self.playoff_type_string = self.json['playoff_type_string']
            self.division_keys = self.json['division_keys']
            self.lat = self.json['lat']
            self.location_name = self.json['location_name']
        except KeyError:
            self.webcasts_json = None
            self.postal_code = None
            self.playoff_type = None
            self.week = None
            self.timezone = None
            self.first_event_id = None
            self.gmaps_place_id = None
            self.short_name = None
            self.end_date = None
            self.gmaps_url = None
            self.address = None
            self.lng = None
            self.website = None
            self.event_type_string = None
            self.parent_event_key = None
            self.playoff_type_string = None
            self.division_keys = None
            self.lat = None
            self.location_name = None

        # Calculated attributes for user convenience
        if self.district_json:
            self.district_district = self.district = District(self.district_json)
        else:
            self.district_district = self.district = None

    def __str__(self):
        return Util.pformat(self)

class District:
    def __init__(self, response):
        self.json = Util.parse(response)

        self.abbreviation = self.json['abbreviation']
        self.display_name = self.json['display_name']
        self.key = self.json['key']
        self.year = self.json['year']

    def __str__(self):
        return Util.pformat(self)

class Robot:
    def __init__(self, response):
        self.json = Util.parse(response)

        self.year = self.json['year']
        self.robot_name = self.json['robot_name']
        self.key = self.json['key']
        self.team_key = self.json['team_key']

    def __str__(self):
        return Util.pformat(self)

class Match:
    def __init__(self, response):
        self.json = Util.parse(response)

        # Data that should be contained in simple or verbose form
        self.key = self.json['key']
        self.comp_level = self.json['comp_level']
        self.set_number = self.json['set_number']
        self.match_number = self.json['match_number']
        self.blue_alliance_json = self.json['alliances']['blue']
        self.red_alliance_json = self.json['alliances']['red']
        self.winning_alliance_color =  self.json['winning_alliance']
        self.event_key = self.json['event_key']
        self.time = self.json['time']
        self.actual_time = self.json['actual_time']
        self.predicted_time = self.json['predicted_time']

        # Data not found in simple form
        try:
            self.post_result_time = self.json['post_result_time']
            self.score_breakdown_json = self.json['score_breakdown']
            self.videos_json = self.json['videos']
        except KeyError:
            self.post_result_time = None
            self.score_breakdown_json = None
            self.videos_json = None

        # Calculated attributes for user convenience
        if self.blue_alliance_json:
            self.blue_alliance = self.blue_alliance_alliance = Alliance(self.blue_alliance_json)
        else:
            self.blue_alliance = self.blue_alliance_alliance = None
        if self.red_alliance_json:
            self.red_alliance = self.red_alliance_alliance = Alliance(self.red_alliance_json)
        else:
            self.red_alliance = self.red_alliance_alliance = None
        if self.winning_alliance_color in self.json['alliances']:
            self.winning_alliance = self.winning_alliance_alliance = Alliance(self.json['alliances'][self.winning_alliance_color])
        if self.videos_json:
            self.videos = [Media(v) for v in self.videos_json]

    def __str__(self):
        return Util.pformat(self)

class Alliance:
    def __init__(self, response):
        self.json = Util.parse(response)

        self.score = self.json['score']
        self.team_keys = self.json['team_keys']
        self.surrogate_team_keys = self.json['surrogate_team_keys']

    def __str__(self):
        return Util.pformat(self)

class Media:
    def __init__(self, response):
        self.json = Util.parse(response)

        self.key = self.json.get('key', None)
        self.type = self.json.get('type', None)
        self.foreign_key = self.json.get('foreign_key', None)
        self.details = self.json.get('details', None)
        self.preferred = self.high_quality = self.json.get('preferred', None)

    def __str__(self):
        return Util.pformat(self)


class Award:
    def __init__(self, response):
        self.json = Util.parse(response)

        self.name = self.json['name']
        self.award_type = self.json['award_type']
        self.event_key = self.json['event_key']
        self.recipient_list = self.recipient_list_json = self.json['recipient_list']
        self.team_keys = [self.recipient_list[i]['team_key'] for i in range(len(self.recipient_list))]
        self.recipient = self.awardee = [self.recipient_list[i]['awardee'] for i in range(len(self.recipient_list))]
        self.year = self.json['year']

    def __str__(self):
        return Util.pformat(self)

class EventStatus:
    def __init__(self, response):
        self.json = Util.parse(response)

        self.qual_json = self.json['qual']
        self.alliance_json = self.json['alliance']
        self.playoff_json = self.json['playoff']
        self.alliance_status_str = self.json['alliance_status_str']
        self.playoff_status_str = self.json['playoff_status_str']
        self.overall_status_str = self.json['overall_status_str']

        if self.qual_json:
            self.qual = EventStatusRank(self.qual_json)
        else:
            self.qual = None
        if self.playoff_json:
            self.playoff = EventStatusPlayoff(self.playoff_json)
        else:
            self.playoff = None
        if self.alliance_json:
            self.alliance_json = EventStatusAlliance(self.alliance_json)

    def __str__(self):
        return Util.pformat(self)

class EventStatusRank:
    def __init__(self, response):
        self.json = Util.parse(response)

        self.num_teams = self.json['num_teams']
        self.ranking_json = self.json['ranking']
        self.sort_order_info = self.json['sort_order_info']
        self.status = self.json['status']
        self.dq = self.ranking_json['dq']
        self.matches_played = self.ranking_json['matches_played']
        self.qual_average = self.ranking_json['qual_average']
        self.rank = self.ranking_json['rank']
        self.record_json = self.ranking_json['record']
        self.sort_orders = self.ranking_json['sort_orders']
        self.team_key = self.ranking_json['team_key']
        self.wins = self.record_json['wins']
        self.losses = self.record_json['losses']
        self.ties = self.record_json['ties']

    def __str__(self):
        return Util.pformat(self)

class EventStatusAlliance:
    def __init__(self, response):
        self.json = Util.parse(response)

        self.name = self.json['name']
        self.number = self.json['number']
        self.backup_json = self.json['backup']
        self.pick = self.json['pick']

        if self.backup_json:
            self.backup = [Backup(b) for b in self.backup_json]
        else:
            self.backup = None

    def __str__(self):
        return Util.pformat(self)

class EventStatusPlayoff:
    def __init__(self, response):
        self.json = Util.parse(response)

        self.level = self.json['level']
        self.record = self.json['record']
        self.status = self.json['status']

    def __str__(self):
        return Util.pformat(self)

class BackupRobot:
    def __init__(self, response):
        self.json = Util.parse(response)

        self.out = self.json['out']
        self.backup = self.json['in']

    def __str__(self):
        return Util.pformat(self)

