import datetime


class Message(object):
    def __init__(self, service, metric, time=None):
        self.service = service
        self.time = time or datetime.datetime.now()
        self.metric = metric

    def to_dict(self):
        return dict(service=self.service,
                    time=self.time.strftime('%Y-%m-%d %H:%M:%S%z'),
                    metric=self.metric)
