import io
import os
from os.path import expanduser

import yaml
from sqlalchemy import create_engine


class Config(object):

    DB_CONNECTION_FORMAT = 'postgresql://{user}:{pass}@{host}:{port}/{name}'

    def __init__(self, config_path):

        home = expanduser("~")
        production = os.path.join(home, "data/configs")
        if os.path.exists(production):
            head, _ = os.path.split(config_path)
            head, _ = os.path.split(head)
            _, tail = os.path.split(head)

            config_path = os.path.join(production,
                                       '{}.yml'.format(tail))

        self.config_path = config_path
        with io.open(config_path, 'r') as cfg:
            self.data = yaml.safe_load(cfg)

        database = self.data.get('db')
        if database:
            self.DATABASE = self.DB_CONNECTION_FORMAT.format(**database)
            self.engine = create_engine(self.DATABASE, echo=True)

        service_session = self.data.get('service_session')
        if service_session:
            self.service_session = service_session

        version = self.application.get('version')
        if version:
            self.version = version

        self.APP_PORT = self.application.get('port')

    @property
    def application(self):
        return self.data.get('application')

    @property
    def db(self):
        return self.data.get('db')

    @property
    def redis_params(self):
        return self.data.get('redis_params')

    @property
    def session_params(self):
        return self.data.get('session_params')
