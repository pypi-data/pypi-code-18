class Config(object):
    def __init__(self, **kwargs):
        self.rabbitmq_host = kwargs.get('rabbitmq_host')
        self.rabbitmq_port = kwargs.get('rabbitmq_port')
        self.rabbitmq_queue = kwargs.get('rabbitmq_queue')
        self.rabbitmq_exchange = kwargs.get('rabbitmq_exchange')
        self.cassandra_endpoints = kwargs.get('cassandra_endpoints')
        self.riemann_host = kwargs.get('riemann_host')
        self.riemann_port = kwargs.get('riemann_port')
