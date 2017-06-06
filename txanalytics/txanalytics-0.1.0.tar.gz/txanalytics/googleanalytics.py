import attr
import treq


class MissingParameterError(Exception):
    pass


@attr.s
class GoogleAnalytics(object):
    url = 'https://www.google-analytics.com/collect'

    # General
    version = attr.ib(default=1)
    tracking_id = attr.ib(default=None)
    anonymize_ip = attr.ib(default=None)
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

    def get_payload(self):
        raise NotImplementedError()

    def get_main_payload(self):
        payload = {
            'v': self.version,
            'tid': self.tracking_id,
        }

        if self.anonymize_ip:
            payload['aip'] = self.anonymize_ip
        if self.data_source:
            payload['ds'] = self.data_source
        if self.queue_time:
            payload['qt'] = self.queue_time

        if self.client_id:
            payload['cid'] = self.client_id
        elif self.user_id:
            payload['uid'] = self.user_id
        else:
            raise MissingParameterError('You must provide either client_id or user_id')

        if self.session_control:
            payload['sc'] = self.session_control
        if self.user_ip:
            payload['uip'] = self.user_ip
        if self.user_agent:
            payload['ua'] = self.user_agent
        if self.geo_id:
            payload['geoid'] = self.geo_id

        return payload

    def track(self):
        payload = self.get_payload()
        payload.update(self.get_main_payload())

        params = {}
        if self.z:
            params['z'] = self.z

        d = treq.post(url=self.url, data=payload, params=params)
        return d


@attr.s
class Event(GoogleAnalytics):
    category = attr.ib()
    action = attr.ib()
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
