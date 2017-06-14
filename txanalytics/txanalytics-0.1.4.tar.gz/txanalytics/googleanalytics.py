import attr
import treq


class MissingParameterError(Exception):
    pass


@attr.s
class GoogleAnalytics(object):
    url = 'https://www.google-analytics.com/collect'

    # General
    tracking_id = attr.ib()
    version = attr.ib(default=1)
    anonymize_ip = attr.ib(default=1)
    data_source = attr.ib(default=None)
    queue_time = attr.ib(default=None)
    z = attr.ib(default=None)

    # User
    client_id = attr.ib(default=None)
    user_id = attr.ib(default=None)

    # Session
    session_control = attr.ib(default=None)
    user_ip = attr.ib(default=None)
    user_agent = attr.ib(default=None)
    geo_id = attr.ib(default=None)

    # Custom Dimensions
    cd1 = attr.ib(default=None)
    cd2 = attr.ib(default=None)
    cd3 = attr.ib(default=None)
    cd4 = attr.ib(default=None)
    cd5 = attr.ib(default=None)
    cd6 = attr.ib(default=None)
    cd7 = attr.ib(default=None)
    cd8 = attr.ib(default=None)
    cd9 = attr.ib(default=None)
    cd10 = attr.ib(default=None)

    @client_id.validator
    def check_client_id(self, attribute, value):
        if value is None and self.user_id is None:
            raise ValueError('client_id and user_id must not be both empty')

    @user_id.validator
    def check_user_id(self, attribute, value):
        if value is None and self.client_id is None:
            raise ValueError('client_id and user_id must not be both empty')

    def get_payload(self):
        raise NotImplementedError()

    def get_main_payload(self):
        payload = {
            'v': self.version,
            'tid': self.tracking_id,
            'aip': self.anonymize_ip,
        }

        if self.data_source:
            payload['ds'] = self.data_source
        if self.queue_time:
            payload['qt'] = self.queue_time

        # We prefer to anonymize users if possible
        if self.client_id:
            payload['cid'] = self.client_id
        elif self.user_id:
            payload['uid'] = self.user_id

        if self.session_control:
            payload['sc'] = self.session_control
        if self.user_ip:
            payload['uip'] = self.user_ip
        if self.user_agent:
            payload['ua'] = self.user_agent
        if self.geo_id:
            payload['geoid'] = self.geo_id

        for i in range(1, 11):
            key = 'cd{}'.format(i)
            if getattr(self, key):
                payload[key] = getattr(self, key)

        return payload

    def track(self):
        payload = self.get_payload()
        payload.update(self.get_main_payload())

        params = {}
        if self.z:
            params['z'] = self.z

        return treq.post(url=self.url, data=payload, params=params)


@attr.s
class Event(GoogleAnalytics):
    category = attr.ib(default=None)
    action = attr.ib(default=None)
    label = attr.ib(default=None)
    value = attr.ib(default=None)

    def get_payload(self):
        payload = {
            't': 'event',
            'ec': self.category,
            'ea': self.action,
        }
        if self.label:
            payload['el'] = self.label
        if self.value is not None:
            payload['ev'] = str(int(self.value))

        return payload
